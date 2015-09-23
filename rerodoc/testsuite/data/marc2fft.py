#!/home/rerodoc/VirtualEnvs/rerodoc/bin/python
# -*- coding: utf-8 -*-

#---------------------------- Modules -----------------------------------------

# import of standard modules
import sys
import os
import copy
import re
import datetime
from optparse import OptionParser
from rero_invenio_tools import Record, Collection, Iterator


__author__ = "Johnny Mariethoz <Johnny.Mariethoz@rero.ch>"
__version__ = "0.0.0"
__copyright__ = "Copyright (c) 2009 Rero, Johnny Mariethoz"
__license__ = "Internal Use Only"


class ImportFile:

    class UnsupportedUrl(Exception):
        pass

    class RestrictedFiles(Exception):
        pass


RESTRICTION = {
    "361": "PA16JU",
    "000": "FRIBOURG",
    "100": "VALAIS",
    "200": "GENEVE",
    "300": "NEUCHATEL",
    "800": "VAUD",
    "900": "RERO_CENTRAL",
    "990": "INTERNAL",
    "999": "RERO"
}


def download_file(url):
    path = url.replace("http://doc.rero.ch/", "")
    print "downloading: %s" % url
    sys.stdout.flush()
    if os.path.isfile(path):
        return os.path.abspath(path)
    directory = re.sub(r"files/.*", "files", path)
    try:
        os.makedirs(directory)
    except:
        pass
    from urllib import urlretrieve
    print path
    urlretrieve(url, path)
    return os.path.abspath(path)


def build_order_fft_tag(recid, full_file_name, n):
    from invenio.bibformat_elements import rero_utils
    internal_files = rero_utils.get_internal_files(int(recid))
    for icon, doc_file in internal_files:
        if doc_file.get_full_name() == full_file_name:
            doc_file_fft_tag = {
                "n": doc_file.get_name(),
                "f": doc_file.get_format(),
                "d": "KEEP-OLD-VALUE",
                "r": "KEEP-OLD-VALUE",
                "z": "order:%d" % n
            }
            icon_fft_tag = {}
            if icon:
                icon_fft_tag = {
                    "n": icon.get_name(),
                    "f": icon.get_format(),
                    "d": "KEEP-OLD-VALUE",
                    "r": "KEEP-OLD-VALUE",
                    "z": "order:%d" % n
                }

            return (icon_fft_tag, doc_file_fft_tag)
    return None


def generate_icon(filepath, mime):
    return None
    from multivio import pdf_processor, image_processor
    result = None
    if mime == 'application/pdf':
        proc = pdf_processor.PdfProcessor(filepath.encode("utf-8"))
        result = proc.render(max_output_size=(80, 80), index={"page_number": 1})
    elif mime.startswith("image"):
        proc = image_processor.ImageProcessor(str(filepath))
        result = proc.render(max_output_size=(80, 80))
    if result:
        filename = os.path.splitext(os.path.basename(filepath))[0]
        out_filename = os.path.join('./tmp_thumb', filename + ".jpg")
        out_file = file(out_filename, "w")
        out_file.write(result[1])
        out_file.close()
        return out_filename
    return None


def lm2fft(record):
    local_files = []
    #remove useless marc field
    if '930__' in record:
        del(record['930__'])

    for f in record["8564_"][:]:
        url = f['u']
        #internal
        if re.search(r'doc.rero.ch', url):
            local_files.append(copy.copy(f))
            record["8564_"].remove(f)
    if not record["8564_"]:
        del(record["8564_"])
    if local_files:
        lf_to_add = to_add(local_files, record.rec_id)
        record["FFT__"] = []
        n = 1
        for lf in local_files:
            if lf in lf_to_add:
                tmp = marc2fft(lf)
                #keep order
                tmp["z"] = "order:%d" % n
                record["FFT__"].append(tmp)
            else:
                #already ingested just update order
                fft_icon, fft_doc = build_order_fft_tag(recid=record.rec_id,
                                                        full_file_name=lf["f"],
                                                        n=n)
                if fft_doc:
                    record["FFT__"].append(fft_doc)
                if fft_icon:
                    record["FFT__"].append(fft_icon)
            n += 1
        #remove non present files
        for tr in to_remove(local_files, record.rec_id):
            record["FFT__"].append(marc2fft(tr, "DELETE"))
    return record


def marc2fft(marc, doc_type=None):
    fft = {}
    if doc_type:
        fft["t"] = doc_type
    fft["n"] = marc['f'].replace(" ", "_")
    if doc_type == "DELETE":
        return fft
    fft["a"] = download_file(marc['u'])
    icon = generate_icon(marc['u'], marc['q'])
    if icon:
        fft["x"] = icon
    fft["d"] = marc['z']

    embargo_regex = re.compile(r"(\w+)\s+restricted access until (\d{4}-\d{2}-\d{2})")
    embargo_match = embargo_regex.match(marc.get("x", ""))
    if embargo_match:
        embargo_restriction, embargo_date = embargo_match.groups()
        fft["r"] = """firerole:
    allow roles /.*,%s,.*/
    allow from "%s"
    allow any
""" % (embargo_restriction.upper(), embargo_date)
    else:
        fft["r"] = ""
    return fft


def to_add(candidates, recid=None):
    if not recid:
        return candidates
    rec = Record(recid)
    to_return = []
    rec_mod_date = datetime.datetime.strptime(rec.mod_date, "%Y-%m-%d %H:%M:%S")
    for c in candidates:
        file_add_date = datetime.datetime.strptime(c['y'], "%Y-%m-%d %H:%M:%S")
        if file_add_date > rec_mod_date:
            to_return.append(c)
    return to_return


def to_remove(candidates, recid=None):
    if not recid:
        return []
    rec = Record(recid)
    to_return = []
    file_names = [fn["f"] for fn in candidates]
    for fulltext in rec["8564_"]:
        if fulltext.get("f") and fulltext.get("u").find("files") and not(fulltext.get("f") in file_names):
            to_return.append(fulltext)
    return to_return


def bibupload(file_name, fg=False):
    #path because multivio set stdout to stderr
    reload(sys)
    from invenio.dbquery import run_sql
    from invenio.bibtask import task_low_level_submission
    bib_id = task_low_level_submission('bibupload', 'invenio_utils', '-r',
                                       '-i', '--verbose', '9', file_name)

    if bib_id:
        sys.stdout.write("Task #%s submitted. \n" % bib_id)
    if fg:
        web_status = run_sql('SELECT status from schTASK where id=%s', (bib_id,))
        import time
        sys.stdout.write("Waiting for bibupload:")
        while web_status[0][0] != 'DONE':
            web_status = run_sql('SELECT status from schTASK where id=%s', (bib_id,))
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(2)

#---------------------------- Main Part ---------------------------------------
if __name__ == '__main__':

    usage = "usage: %prog [options]"

    parser = OptionParser(usage)

    parser.set_description("Change It")

    parser.add_option("-v", "--verbose", dest="verbose", help="Verbose mode",
                      action="store_true", default=False)

    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("Error: incorrect number of arguments, try --help")

    col = Collection()
    for rec in Iterator(file(args[0])):
        try:
            del (rec["0248_"])
            rec.rec_id = None
            new_rec = lm2fft(rec)
            col.append(new_rec)
            #out_file = args[0] + ".tmp"
            #c = Collection()
            #c.append(new_rec)
            #c.save(out_file)
            #bibupload(out_file)
        except Exception as msg:
            #err_file = \
            #    file("/home/rerodoc/web/doc.submit.rero.ch/log/bibupload.err", "a")
            #err_file.write("Error for: %s\n" % args[0])
            #err_file.write(str(msg)+"\n")
            sys.stderr.write("Error: " + str(msg) + "\n")
            sys.exit(1)
    col.save(args[1])
    sys.exit(0)

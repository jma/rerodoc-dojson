wget "http://doc.rero.ch/search?ln=fr&sc=1&p=recid%3A232386->232586 not 980__a:JOURNAL&action_search=&of=xm&rg=200" -O rerodoc.xml
python marc2fft.py rerodoc.xml demo_record_marc_data.xml

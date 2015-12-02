app = angular.module('test', ['schemaForm', 'ui.bootstrap', 'jsonrpc'])
.config(function(schemaFormProvider, schemaFormDecoratorsProvider, sfBuilderProvider) {
 schemaFormDecoratorsProvider.addMapping(
   'bootstrapDecorator',
   'autocomplete',
   '/static/js/templates/autocomplete.html'
   );
 schemaFormDecoratorsProvider.createDirective(
   'autocomplete',
   '/static/js/templates/autocomplete.html'
   );
//template should be in cache
//           schemaFormDecoratorsProvider.defineAddOn(
//             'bootstrapDecorator',
//              'autocomplete',
//              '/static/templates/autocomplete.html',
//              sfBuilderProvider.stdBuilders
//           );
});
Add the following code in plugin.py to have custom JS and CSS resources in your plug-in

1. Implement IResource in your plug-in class definition:

    ```python
    class myPlugin(plugins.SingletonPlugin):    
        plugins.implements(plugins.IResource)
    ```

    

2. Add and edit the following code to the plug-in implementation

    ```python
    def add_libraries(self, config):
        libraries = [u.add_library("my_plugin_library", "resources")]
        return libraries
    
    def add_js_resources(self, config):
        my_plugin_js = [
            u.add_js_resource("my_plugin", "my_js_resource", "relative/path/to/resources/my_js_resource.js", None)
        ]
        return my_plugin_js
    
    def add_css_resources(self, config):
        my_plugin_css = [
            u.add_css_resource(
                "my_plugin", "my_css_resource", "relative/path/to/resources/my_js_resource.css", None
            )
        ]
        return my_plugin_css
    ```

    

3. In your Jinja2 templates you can inject your resources with
    
    ```jinja2
    {% jsresource request,'my_plugin_library','my_js_resource' %}
    {% cssresource request,'my_plugin_library','my_css_resource' %}
    ```
    
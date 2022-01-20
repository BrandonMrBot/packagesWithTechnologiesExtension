Add the following code in plugin.py to have custom static resources in your plug-in

1. Add the following line to the function "update_config":

    ```python
    u.add_static_view(config, "my_plugin_static_library", "static")
    ```

2. Copy the static files into the "static" directory of the plugin

3. In your Jinja2 templates you can inject your static files with

    
    ```jinja2
    {{request.url_for_static('my_static_file.jpg','my_plugin_static_library')}}
    ```
    
    


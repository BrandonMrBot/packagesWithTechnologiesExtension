- Extract the messages from your plug-in. Run every time you have new strings in your code to translate

  ```shell
  python setup.py extract_messages
  ```

- Initialize the catalog. (Run **only once** for each language code). Replace [language_code] with a code from [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) . You need to run this if you want to provide a new language. **If you run this with an existing language code your previous translations will be deleted**

  ```shell
  python setup.py init_catalog -l [language_code]
  ```

  This will create a .po file in the "locale" directory of your plug-in

- Update the catalog. Run every time you run "extract_messages"

  ```shell
  python setup.py update_catalog
  ```

  This will move the newly extracted messages collected by "extract_messages" to each .po file

- Translate each of the .po files for each language in the "locale" directory. You can use tools like:
  - [PoEditor](https://poeditor.com/)
  - [Lokalize](https://kde.org/applications/en/office/org.kde.lokalize)
  - [PoEdit](https://poedit.net/)
  - [GTranslator](https://wiki.gnome.org/Apps/Gtranslator)

- Compile the catalog. Run once after deployment. 

  ```shell
  python setup.py compile_catalog
  ```

  This will create a .mo files for each .po file. These files should not be tracked by git therefore this command should be called after deployment.


# Image selector tool

Invoke with `./image_selector.py <source_dir>`

Controls:

- Left and Right arrows list the pictures
- Space toggles selection for each picture
- The checkbox shouldn't be clicked on
- Ctrl+w exits the tool and saves the list of images at `selection_<timestamp>.txt`

To copy images after you've made a selection do:

`cat selection_<timestamp>.txt | xargs cp -t <target_dir>`

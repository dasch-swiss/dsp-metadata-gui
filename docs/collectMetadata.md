# Documentation for 'Metadata GUI'

## The GUI Classes

The DSP-Metadata-GUI is managed by a set of classes within the module collectMetadata.py and other
classes. In this page we introduce the GUI classes.

There are the following classes:

- ProjectFrame
- ProjectPanel
- TabOne
- PropertyRow
- DataTab
- HelpPopup
- TabbedWindow


The Class ProjectFrame manages the frame with the menu bar. A runner class 
(not shown here) collectMetadata() launches the app.

<!-- In the mkdocstrings documentation (Usage, etc.) the path to the class is given as
    ::: collectMetadata.ProjectFrame and explicitly allows to address a Class. 
    In this directive there are two mistakes: Between the module and the Class there
    should be a colon, and classes may not be addressed. You must mention the function,
    otherwise it does not work, at least for me it did never work... -->

## Documentation for Class 'ProjectFrame'

::: collectMetadata:ProjectFrame.__init__
    rendering:
        show_root_heading: false
        show_source: false

::: collectMetadata:ProjectFrame.create_menu

::: collectMetadata:ProjectFrame.on_save






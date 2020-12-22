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


<!-- The Class ProjectFrame manages the frame with the menu bar. A runner class 
(not shown here) collectMetadata() launches the app. -->

<!-- In the mkdocstrings documentation (Usage, etc.) the path to the class is given as
    ::: collectMetadata.ProjectFrame and explicitly allows to address a Class. 
    In this directive there are two mistakes: Between the module and the Class there
    should be a colon, and classes may not be addressed. You must mention the function,
    otherwise it does not work, at least for me it did never work... -->

## Main Function

::: dspMetadataGUI.collectMetadata:collectMetadata
    <!-- rendering:
        show_root_heading: true
        show_root_full_path: false
        heading_level: 3
        show_source: false -->

## Class 'ProjectFrame'


::: dspMetadataGUI.collectMetadata:ProjectFrame.__init__
    <!-- rendering:
        show_source: false -->

<!-- ### create_menu()

::: dspMetadataGUI.collectMetadata:ProjectFrame.create_menu

### on_save()

::: dspMetadataGUI.collectMetadata:ProjectFrame.on_save -->

## Class 'ProjectPanel'

<!-- 
This class manages the window content. It displays a list of projects, which are selectable
and provides an edit button. -->

<!-- ### __init__() -->

::: dspMetadataGUI.collectMetadata:ProjectPanel.__init__
    <!-- rendering:
        show_source: false -->

<!-- ### on_add_new_project()

::: dspMetadataGUI.collectMetadata:ProjectPanel.on_add_new_project -->

::: dspMetadataGUI.collectMetadata:ProjectPanel.refresh_repos

::: dspMetadataGUI.collectMetadata:ProjectPanel.create_header

::: dspMetadataGUI.collectMetadata:ProjectPanel.load_view

::: dspMetadataGUI.collectMetadata:ProjectPanel.on_edit_tabbed

::: dspMetadataGUI.collectMetadata:ProjectPanel.on_process_data

::: dspMetadataGUI.collectMetadata:ProjectPanel.add_new_project

::: dspMetadataGUI.collectMetadata:ProjectPanel.on_remove_project

::: dspMetadataGUI.collectMetadata:ProjectPanel.on_validate

## Class TabOne

::: dspMetadataGUI.collectMetadata:TabOne.show_help

::: dspMetadataGUI.collectMetadata:TabOne.add_file

::: dspMetadataGUI.collectMetadata:TabOne.remove_file

## Class PropertyRow

::: dspMetadataGUI.collectMetadata:PropertyRow.__init__

### data_class() 

::: dspMetadataGUI.collectMetadata:PropertyRow.data_class

### prop()

::: dspMetadataGUI.collectMetadata:PropertyRow.prop

### get_value()

::: dspMetadataGUI.collectMetadata:PropertyRow.get_value

### refresh_ui()

::: dspMetadataGUI.collectMetadata:PropertyRow.refresh_ui

### refresh_chocie()

::: dspMetadataGUI.collectMetadata:PropertyRow.refresh_choice

### validate()

::: dspMetadataGUI.collectMetadata:PropertyRow.validate

### set_value()

::: dspMetadataGUI.collectMetadata:PropertyRow.set_value

### onValueChange()

::: dspMetadataGUI.collectMetadata:PropertyRow.onValueChange

## Class DataTab

:::dspMetadataGUI.collectMetadata:DataTab.__init__

### active_dataset()

:::dspMetadataGUI.collectMetadata:DataTab.active_dataset

### update_data()

:::dspMetadataGUI.collectMetadata:DataTab.update_data

### refresh_ui()

:::dspMetadataGUI.collectMetadata:DataTab.refresh_ui

### add_object()

:::dspMetadataGUI.collectMetadata:DataTab.add_object

### remove_object()

:::dspMetadataGUI.collectMetadata:DataTab.remove_object

### change_selection()

:::dspMetadataGUI.collectMetadata:DataTab.change_selection

### add_to_list()

:::dspMetadataGUI.collectMetadata:DataTab.add_to_list

### reset_widget()

:::dspMetadataGUI.collectMetadata:DataTab.reset_widget

### remove_from_list()

:::dspMetadataGUI.collectMetadata:DataTab.remove_from_list

### show_help()

:::dspMetadataGUI.collectMetadata:DataTab.show_help

### show_validity()

:::dspMetadataGUI.collectMetadata:DataTab.show_validity

### pic_date()

:::dspMetadataGUI.collectMetadata:DataTab.pick_date

## Class HelpPopup

:::dspMetadataGUI.collectMetadata:HelpPopup.__init__

## Class TabbedWindow

:::dspMetadataGUI.collectMetadata:TabbedWindow.__init__

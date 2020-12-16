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

## Class 'ProjectFrame'

::: collectMetadata:ProjectFrame.__init__
    rendering:
        show_root_heading: false
        show_source: false

### create_menu()

::: collectMetadata:ProjectFrame.create_menu

### on_save()

::: collectMetadata:ProjectFrame.on_save

## Class 'ProjectPanel'

This class manages the window content. It displays a list of projects, which are selectable
and provides an edit button.

### on_add_new_project()

::: collectMetadata:ProjectPanel.on_add_new_project

::: collectMetadata:ProjectPanel.display_repos

::: collectMetadata:ProjectPanel.create_header

::: collectMetadata:ProjectPanel.load_view

::: collectMetadata:ProjectPanel.on_edit_tabbed

::: collectMetadata:ProjectPanel.on_process_data

::: collectMetadata:ProjectPanel.add_new_project

::: collectMetadata:ProjectPanel.on_remove_project

::: collectMetadata:ProjectPanel.on_validate

## Class TabOne

::: collectMetadata:TabOne.show_help

::: collectMetadata:TabOne.add_file

::: collectMetadata:TabOne.remove_file

## Class PropertyRow

::: collectMetadata:PropertyRow.__init__

### data_class() 

::: collectMetadata:PropertyRow.data_class

### prop()

::: collectMetadata:PropertyRow.prop

### get_value()

::: collectMetadata:PropertyRow.get_value

### refresh_ui()

::: collectMetadata:PropertyRow.refresh_ui

### refresh_chocie()

::: collectMetadata:PropertyRow.refresh_choice

### validate()

::: collectMetadata:PropertyRow.validate

### set_value()

::: collectMetadata:PropertyRow.set_value

### onValueChange()

::: collectMetadata:PropertyRow.onValueChange

## Class DataTab

:::collectMetadata:DataTab.__init__

### active_dataset()

:::collectMetadata:DataTab.active_dataset

### update_data()

:::collectMetadata:DataTab.update_data

### refresh_ui()

:::collectMetadata:DataTab.refresh_ui

### add_object()

:::collectMetadata:DataTab.add_object

### remove_object()

:::collectMetadata:DataTab.remove_object

### change_selection()

:::collectMetadata:DataTab.change_selection

### add_to_list()

:::collectMetadata:DataTab.add_to_list

### reset_widget()

:::collectMetadata:DataTab.reset_widget

### remove_from_list()

:::collectMetadata:DataTab.remove_from_list

### show_help()

:::collectMetadata:DataTab.show_help

### show_validity()

:::collectMetadata:DataTab.show_validity

### pic_date()

:::collectMetadata:DataTab.pick_date

## Class HelpPopup

:::collectMetadata:HelpPopup.__init__

## Class TabbedWindow

:::collectMetadata:TabbedWindow.__init__

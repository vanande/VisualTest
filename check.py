import Libs.PyVisualAutomation as va

project = va.sys.argv[1]
element_searched = va.sys.argv[2]
field_width = va.sys.argv[3]
field_height = va.sys.argv[4]
w_marge = va.sys.argv[5]
h_marge = va.sys.argv[6]
seconds = va.sys.argv[7]

va.initialize(project)

elements_found = va.check_elements(field_width=field_width, field_height=field_height, w_marge=w_marge, h_marge=h_marge, seconds=seconds, element_searched=element_searched, save=True, show_process=True)

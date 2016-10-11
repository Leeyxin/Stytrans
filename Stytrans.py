import sublime
import sublime_plugin


class StytransCommand(sublime_plugin.TextCommand):

    def run(self, edit, style_name):
        sels = self.view.sel()
        for sel in sels:
            the_string = self.view.substr(sel)
            changer = StyleChanger(the_string)
            func = getattr(changer, style_name, None)
            if func:
                new_string = func()
                region = sublime.Region(sel.begin(), sel.end())
                self.view.replace(edit, region, new_string)


class StyleChanger:

    def __init__(self, the_string):
        self.string = the_string
        self.wd_list = self.to_wd_lis()

    def to_wd_lis(self):
        # to find all word in theString
        all_wd_lis = []
        index_lis = []
        if "_" in self.string:
            for index, value in enumerate(self.string):
                if index == 0 or value == "_":
                    index_lis.append(index)
        else:
            for index, value in enumerate(self.string):
                if index == 0 or not value.islower():
                    index_lis.append(index)

        max_index = len(index_lis) - 1
        for i, index in enumerate(index_lis):
            if i > max_index:
                break
            if i == max_index:
                the_wd = self.string[index:]
            else:
                the_wd = self.string[index:index_lis[i + 1]]
            all_wd_lis.append(the_wd.strip("_"))
        return all_wd_lis

    def to_camel_case_upper(self):
        new_wd_list = [wd.capitalize() for wd in self.wd_list]
        return "".join(new_wd_list)

    def to_cammel_case_lower(self):
        new_wd_list = [wd.capitalize() for wd in self.wd_list]
        new_wd_list[0] = new_wd_list[0].lower()
        return "".join(new_wd_list)

    def to_underscore_notation_upper(self):
        new_wd_list = [wd.upper() for wd in self.wd_list]
        return "_".join(new_wd_list)

    def to_underscore_notation_lower(self):
        new_wd_list = [wd.lower() for wd in self.wd_list]
        return "_".join(new_wd_list)

    def get_oragin_style(self):
        return self.string

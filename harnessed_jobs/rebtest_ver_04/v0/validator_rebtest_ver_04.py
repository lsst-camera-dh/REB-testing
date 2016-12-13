#!/usr/bin/env python
import os
import glob
import subprocess
from collections import OrderedDict

class TsRebException(RuntimeError):
    pass

class TsRebProducts(object):
    "Class to aggregate and parse data products from rebtest code."
    def __init__(self, reb_id=None):
        if reb_id is None:
            self.reb_id = int(os.environ["LCATR_UNIT_ID"].split("-")[-1])
        else:
            self.reb_id = int(reb_id)
        self._get_files()

    def _get_files(self):
        cmd = "ls -rtd ./reb_%02i_* | tail -1" % self.reb_id
        data_lst = subprocess.check_output(cmd, shell=True).strip()
        if not data_lst:
            raise TsRebException("No rebtest data products found.")

        dirname = os.path.basename(data_lst)
        parsed_dirname = dirname.split("_")
        if len(parsed_dirname) != 6 and len(parsed_dirname) != 4:
            raise TsRebException("Bad rebtest dirname: %s" % dirname)

        self.pdf_report = glob.glob(os.path.join(dirname, "*.pdf"))
        self.raw_data = glob.glob(os.path.join(dirname, "data", "*.csv"))
        self.raw_data.extend(glob.glob(os.path.join(dirname, "data", "*.fits")))
        self.tsreb_version = glob.glob(os.path.join(dirname, "data",
                                                    "*VERSION*"))[0]
        self.tex_file = glob.glob(os.path.join(dirname, "data", "*.tex"))[0]

    def _parse_version_file(self):
        ret_dict = OrderedDict()
        with open(self.tsreb_version, "r") as fp:
            for l in fp:
                lsplit = l.split(": ")
                if len(lsplit) != 2:
                    raise TsRebException("ERROR: Invalid version file format")
                ret_dict["version_" + lsplit[0]] = lsplit[1].strip()
        return ret_dict

    def _parse_tex_file(self):
        summary_table = []
        in_table = False
        in_section = False

        with open(self.tex_file, "r") as fp:
            for l in fp:
                if "\\bottomrule" in l and in_table and in_section:
                    break

                if in_section and in_table:
                    summary_table.append(l.strip())

                if "\section{Summary}" in l:
                    in_section = True
                elif in_section and "\midrule" in l:
                    in_table = True

        ret_dict = OrderedDict()
        for l in summary_table:
            results = l.split("&")
            passfail = results[0].split(" ")[1].strip("\'")
            measurment = results[1]
            measurment = measurment.replace("{", "").replace("}", "")
            ret_dict[measurment] = passfail

        return ret_dict

    def get_results_dict(self):
        res_dict = self._parse_tex_file()
        res_dict.update(self._parse_version_file())
        return res_dict

    def get_file_list(self):
        lst = self.pdf_report
        lst.extend(self.raw_data)
        return lst

if __name__ == "__main__":
    import lcatr.schema

    tsreb_products = TsRebProducts()

    results = [lcatr.schema.fileref.make(item)
               for item in tsreb_products.get_file_list()]
    results.append(lcatr.schema.valid(lcatr.schema.get('rebtest_ver_04'),
                                      **tsreb_products.get_results_dict()))

    lcatr.schema.write_file(results)
    lcatr.schema.validate_file()

import pandas as pd
import re
from tzlocal import get_localzone
from pytz import all_timezones

from bdf_utils import get_attribute_check

def ebs_read_tbe(flin='./Dku_bluesky_analysis/saq_bluesky_bgd_20211001_20230430_inv_tbe.csv', flsource='extdata', tblselect=None):
    """
    Read tbe file

    By default: All table names will be converted to lower case
    "Timeseries" table will load into tb (data) and tc (metadata)
    Other tables will load into eg. tb_sites and tc_sites

    Returns a dictionary "result" containing data dataframes (tc_...) and associated metadata (tc_...) or an error message

    Variable name conventions:
    Prefixes:
    tf: table read using pandas read_csv
    tf_tbl: single table read
    tb: dataframe of data
    tc: dataframe of metadata

    hdr: header variables
    att: attribute variables (aka metadata)
    cmt: comments

    i...: index of row in the file
    n...: number of records/rows/attributes

    Parameters:
    - flin: File name (default: '/Users/stuart/Desktop/python_tbe/Dku_bluesky_analysis/saq_bluesky_bgd_20211001_20230430_inv_tbe.csv')
    - flsource: Source: 'extdata' or directory (default: 'extdata')
    - tblselect: Null: Read all tables, or name of table to read

    Returns:
    - result: Dictionary of dataframes with tables and metadata, error: Error Message
    """

    result = {}  # initialize output

    # if flsource == 'extdata':
    #     flin_full = pkg_resources.resource_filename('Aqsebs', f'extdata/{flin}')
    #     if not os.path.exists(flin_full):
    #         return {'result': None, 'error': f'File not found: {flin}'}
    # else:
    #     flin_full = os.path.join(flsource, flin)

    # if not os.path.isfile(flin_full):
    #     return {'result': None, 'error': f'File not found: {flin_full}'}
    # else:
    #     print(f'Will read file {flin_full}')

    # read and parse header column, read second column to fill in missing EOT:
    tf = pd.read_csv(flin, header=None, sep=',', usecols=[0, 1], keep_default_na=False)
    nrecs = len(tf)
    print(tf)
    tf_codes = tf[0].str[:3]
    tf_description = tf[0].str[4:]
    itbl_header = tf_codes[tf_codes == 'TBL'].index
    ntables = len(itbl_header)

    for ntbl in range(1, ntables + 1):
        iheader = itbl_header[ntbl - 1]
        tbl_str = tf_description[iheader].lower()
        if tblselect is not None and tbl_str != tblselect.lower():
            print(f'Skipping table {tbl_str}')
            continue

        # get last possible row in this table: either the row preceding the next table, or the end of the file:
        if ntbl < ntables:
            ilast = itbl_header[ntbl] - 1
        else:
            ilast = nrecs

        # Find end of data:
        ieot = (tf_codes[(iheader + 1):ilast] == 'EOT').idxmax()
        skipdata = False
        if pd.notnull(ieot):
            iend = iheader + ieot
        else:
            inotblank = ((tf[1][(iheader + 1):ilast] != '') & (tf[0][(iheader + 1):ilast] == '')).idxmax()
            if pd.notnull(inotblank):
                iend = iheader + inotblank
                print(f'EOT not found for table {ntbl}/{ntables}, using iend = {iend}')
            else:
                inotblank2 = (tf[1][(iheader + 1):ilast] != '').idxmax()
                if pd.notnull(inotblank2):
                    iend = iheader + inotblank2
                    print(f'Found metadata but no data for table {ntbl}/{ntables}, using iend = {iend}')
                    skipdata = True
                else:
                    print(f'No data and no metadata found for table {ntbl}/{ntables} (consider fixing your file)')
                    continue

        # Find start of data:
        if skipdata:
            # set istart to after table so all attributes are read
            istart = iend + 1
            ndata = 0
        else:
            ibgn = (tf_codes[(iheader + 1):iend] == 'BGN').idxmax()
            if pd.notnull(ibgn):
                istart = iheader + ibgn
            else:
                iblank = (tf[0][(iheader + 1):iend] == '').idxmax()
                if pd.notnull(iblank):
                    # Use first row with blank code in the first column:
                    istart = iheader + iblank
                else:
                    # only one row of data signaled by EOT
                    istart = iend
                    print(f'BGN not found for table {ntbl}/{ntables}, using istart = {istart}')
            ndata = iend - istart + 1

        # Read column names:
        hdr_all = pd.read_csv(flin, header=None, sep=',', skiprows=iheader, nrows=1, keep_default_na=False)
        tbl_name = hdr_all[0].str.replace('^TBL ', '')
        tbl_name = tbl_name.str.replace('\s', '_')
        hdr_select = hdr_all.columns[~hdr_all.isna().any()]
        hdr = hdr_all[hdr_select].reset_index(drop=True)
        hdr[0] = 'TBL_' + tbl_name
        hdr_data = hdr_all[hdr_select].reset_index(drop=True)

        # Find and read metadata:
        itbl_sites = (tf_codes == 'TBL Sites').idxmax()
        ibgn = (tf_codes == 'BGN').idxmax()

        if pd.notnull(itbl_sites) and pd.notnull(ibgn):
            iatt_start = itbl_sites + 1
            iatt_end = ibgn - 1
            att_indices = (tf_codes[iatt_start:iatt_end] == 'ATT')

            if not att_indices.any():
                print(f"No 'ATT' rows found between 'TBL Sites' and 'BGN' for table {ntbl}/{ntables}")
                continue  # Skip to the next table

            iatt = att_indices.idxmax()
        else:
            print(f"'TBL Sites' or 'BGN' row not found for table {ntbl}/{ntables}")
            #continue  # Skip to the next table
            if pd.notnull(iatt):
                iatt1 = iatt + iheader
                iatt2 = iheader + (tf_codes[(iheader + 1):(istart - 1)] == 'ATT').last_valid_index()
                natt = iatt2 - iatt1 + 1
                att = pd.read_csv(flin, header=None, sep=',', skiprows=iatt1, nrows=natt, usecols=hdr_select,
                                keep_default_na=False)
                att.columns = hdr.iloc[0]
                att = att.iloc[iatt - iatt1]
                att.columns = hdr_data.iloc[0]
                att_trans = att.transpose().reset_index()
                att_trans.columns = att_trans.iloc[0]
                att_trans = att_trans[1:]
                att_trans.columns.values[0] = 'Variable'
            else:
                print(f'No attributes found for Table {ntbl}/{ntables}')
                att_trans = None

        # Read data:
        if ndata > 0:
            tf_tbl = pd.read_csv(flin, header=None, sep=',', skiprows=istart, nrows=ndata, usecols=hdr_select,
                                 keep_default_na=False)
            tf_tbl_codes = tf_tbl[0].str[:3]
            icmt = tf_tbl_codes == 'CMT'
            ncmt = icmt.sum()
            if ncmt > 0:
                print(f'Removing {ncmt} comments from table {tbl_str}')
                tf_tbl = tf_tbl[~icmt]
            tf_tbl.drop(columns=0, inplace=True)
            tf_tbl.columns = hdr_data.iloc[0]
            # reset timezones for all dates:
            for col in tf_tbl.columns:
                rtn = get_attribute_check(att_trans, col, 'Units')
                if rtn is None or pd.isnull(rtn['result']):
                    continue
                if tf_tbl[col].dtype == 'datetime64[ns]':
                    tzone = re.match(r'Time\s*\(\s*(.*)\s*\)', rtn['result'])
                    if tzone:
                        tzone = tzone.group(1)
                        if tzone in all_timezones:
                            print(f'Found valid time and timezone ({tzone}) for column {col}')
                            tf_tbl[col] = tf_tbl[col].dt.tz_localize(get_localzone()).dt.tz_convert(tzone)
                        else:
                            print(f'Invalid timezone ({tzone}) for column {col}, leave as is')
                    elif rtn['result'] in all_timezones:
                        tzone = rtn['result']
                        print(f'Inferred time, found timezone ({tzone}) for column {col}')
                        tf_tbl[col] = tf_tbl[col].dt.tz_localize(get_localzone()).dt.tz_convert(tzone)
                    else:
                        print(f'WARNING: No timezone found for variable {col}, leave as is')
                else:
                    continue
        else:
            tf_tbl = None

        # Add data to result:
        if tf_tbl is None:
            result[tbl_str] = None
        elif tbl_str.lower() == 'global':
            tb_gbl = tf_tbl.transpose().reset_index()
            result[tbl_str] = tb_gbl.rename(columns={0: 'Variable'})
        else:
            result[tbl_str] = tf_tbl

        if att_trans is None:
            result['tc_' + tbl_str] = None
        else:
            result['tc_' + tbl_str] = att_trans

        # Summary message:
        print(f'Tables {tbl_str} and tc_{tbl_str} for table {ntbl}/{ntables}: {tf_description[iheader]}')
        if ndata > 0:
            print(f'  Rows: header at {iheader}, data from {istart} to {iend}')
        elif att_trans is not None:
            print(f'  Rows: header at {iheader}, metadata only from {iatt1} to {iatt2}')
        else:
            print(f'  Rows: header only at {iheader}, no data, no metadata')

    print(f'Finished reading file: {flin}')
    return {'result': result, 'error': None}
ebs_read_tbe()
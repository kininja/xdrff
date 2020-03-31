# xdrff
XDR query results reformatter

The xdrff python script fixes the timestamp field in the tab-separated file XDR query results outputs. Without doing this, it’s really hard to sort events by time. 

Example problem and solution is below in the code snippet (from the xdrff.fix.__doc__). The output format is still tab-separated as there are multiple fields with commas and quotes which would otherwise be lost if converting to csv. 


    For example, the default XDR 2 query results outputs useful data, 
    but with the first column formatted like so:

        | Timestamp              |
        | Mar 24th 2020 05:00:13 |

    Sorting or filtering on this column in a spreadsheet is impossible. 
    This function, and the functions it calls, will output the tsv file 
    with a fixed header and column data to match:

        | Month | Day  | Year | Hour | Minute | Second |
        | Mar   | 24th | 2020 | 5    | 0      | 13     |
 

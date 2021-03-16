Backend sample application:

problem: invoice file is being rejected due to:
    1.wrong dispatched partnumber
    2.wrong ordered partnumber
    3.wrong ordered partnumber quantity

Business
    main_event
        get file of orders to be invoiced until EOF
            get dispatched partnumber from Wings
            get ordered partnumber from Wings
            get ordered quantity from ARPW
            write output file to POPIMS

    partnumber
        Partnumber Business Rules to attend different formats according to data dictionary of each application (Wings, POPIMS, OWS)
            converts partnumber POPIMS format 'Basic   /Pref/Su/fix' to WINGS 'Pref/Basic   /Su/fix'
            converts partnumber WINGS format 'Pref/Basic   /Su/fix' to POPIMS 'Basic   /Pref/Su/fix'
            converts partnumber WINGS format 'Pref/Basic   /Su/fix' to OWS format PrefBasicSufix

input/output (for information purpose only)
    connects to SQL Server DB (WINGS)
    connects to Oracle DB (ARPW)
    read txt flat file (POPIMS)... located at the directory IO
    write txt flat file (POPIMS)... located at the directory IO

DAO
    run SELECT query against SQL Server (WINGS), for 2 different business purposes:
        get dispatched partnumber to invoice
        get ordered partnumber
    run SELECT query agains Oracle (ARPW):
        get ordered quantity

Bean_TO (transfer object)
    file_register
        Class Bean to Transfer Object giving input/output POPIMS txt flat file layout
        
unittest on Business
    test_partnumber tests the 3 methods of partnumber conversion to aquire partnumber from different applications

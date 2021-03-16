## MVG/Satimo to ADF conversion utility	
This antenna utility converts MVG/Satimo CSV files into TIA/EIA-804-B standard ADF files.

[ADF antenna standard](https://cloudrf.com/files/ADF_antenna_standard_wg16_99_050.pdf)

To use, take a raw CSV file and call the script with one argument of the filename:

    python3 satimo2adf.py {raw.csv}
    
The script outputs ADF file to stdout which you can redirect to a file eg. > manufacturer_model.adf. Upload these at CloudRF to use them in the service.
![ADF polar plot from CloudRF.com](https://cloudrf.com/files/antenna_plot.jpg)



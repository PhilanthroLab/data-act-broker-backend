import csv
from dataactvalidator.filestreaming.fieldCleaner import FieldCleaner

class LoaderUtils:
    @staticmethod
    def checkRecord (record, fields) :
        """ Returns True if all elements of fields are present in record """
        for data in fields:
            if ( not data in record ):
                return False
        return True

    @staticmethod
    def compareRecords (recordA,recordB, fields) :
        """ Compares two dictionaries based of a field subset """
        for data in fields:
            if (  data in recordA and  data in recordB   ):
                if( not recordA[data]== recordB[data]) :
                    return False
            else :
                return False
        return True

    @classmethod
    def loadCsv(cls,filename,model,interface,fieldMap,fieldOptions):
        """ Loads a table based on a csv

        Args:
            filename: CSV to load
            model: ORM object for table to be loaded
            interface: interface to DB table is in
            fieldMap: dict that maps columns of the csv to attributes of the ORM object
            fieldOptions: dict with keys of attribute names, value contains a dict with options for that attribute.
                Current options are "pad_to_length" which if present will pad the field with leading zeros up to
                specified length, and "skip_duplicate" which ignores subsequent lines that repeat values.
        """
        # Delete all records currently in table
        interface.session.query(model).delete()
        interface.session.commit()
        valuePresent = {}
        # Open csv
        with open(filename,'rU') as csvfile:
            # Read header
            header = csvfile.readline()
            # Split header into fieldnames
            rawFieldNames = header.split(",")
            fieldNames = []
            # Clean field names
            for field in rawFieldNames:
                fieldNames.append(FieldCleaner.cleanString(field))
            # Map fieldnames to attribute names
            attributeNames = []
            for field in fieldNames:
                if field in fieldMap:
                    attributeNames.append(fieldMap[field])
                    if fieldMap[field] in fieldOptions and "skip_duplicates" in fieldOptions[fieldMap[field]]:
                        # Create empty dict for this field
                        valuePresent[fieldMap[field]] = {}
                else:
                    raise KeyError("".join(["Found unexpected field ", str(field)]))
            # Check that all fields are present
            for field in fieldMap:
                if not field in fieldNames:
                    raise ValueError("".join([str(field)," is required for loading table ", str(type(model))]))
            # Open DictReader with attribute names
            reader = csv.DictReader(csvfile,fieldnames = attributeNames)
            # For each row, create instance of model and add it
            for row in reader:
                skipInsert = False
                for field in fieldOptions:
                    # For each field with options present, modify according to those options
                    options = fieldOptions[field]
                    if "pad_to_length" in options:
                        padLength = options["pad_to_length"]
                        row[field] = cls.padToLength(row[field],padLength)
                    if "skip_duplicates" in options:
                        if row[field] in valuePresent[field]:
                            # Value already exists, skip it
                            skipInsert = True
                        else:
                            # Insert new value
                            valuePresent[field][row[field]] = True
                    record = model(**row)
                if not skipInsert:
                    interface.session.merge(record)
            interface.session.commit()

    @staticmethod
    def padToLength(data,padLength):
        """ Pad data with leading zeros

        Args:
            data: string to be padded
            padLength: length of string after padding

        Returns:
            padded string of length padLength
        """

        if len(data) < padLength:
            numZeros = padLength - len(data)
            zeros = "0" * numZeros
            result = zeros + str(data)
            return result
        elif len(data) > padLength:
            raise ValueError("".join(["Value is too long: ",str(data)]))
        else:
            # Data is correct length already
            return data

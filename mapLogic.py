
import json

from CodeList import pack_type_codeList
from ifcsumTemplate import *
from datetime import datetime



# Some Reusable Function:
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data

def write_data_to_file(data, file_path):
    with open(file_path, 'w') as file:
        file.write(str(data))

def modifyDateTimeFormat(inDateTime,inFormat,outFormat):
        date_str=inDateTime
        datetime_obj = datetime.strptime(date_str, inFormat)
        return (str(datetime_obj.strftime(outFormat))+"?+00?:00")


def split_string(string, chunk_length):
    return [string[i:i+chunk_length] for i in range(0, len(string), chunk_length)]


# Example usage
file_path = 'C:\\Users\\rakro\\Desktop\\EDI Parsing using Python\\IFCSUM_Template_Creation\\Input\\VEN-125468_IFCSUM.json'  # Replace with the path to your JSON file
json_data = read_json_file(file_path)


# Creation of main Object
ediData = EDIData("IFCSUM","D","99B","BNS00019","GEODIST")

# Now Insert all the Segment With Logic:


#----------------------------------------------------------------Mapping Logic Starts Here----------------------------------------------------------------

bgm = BGM()
bgm.document_name_code_01_01="335"
bgm.document_number_02_01=json_data[0]["BookingReference"]
bgm.message_function_code_03="9"
ediData.add_segment(bgm)

dtm= DTM()
dtm.dateTime_code_qualifier_01_01="137"
dtm.dateTime_value_01_02=modifyDateTimeFormat(json_data[0]["BookingSubmitted"],"%Y-%m-%dT%H:%M:%S.%fZ","%Y%m%d%H%M%S")
dtm.dateTime_Format_01_03="304"
ediData.add_segment(dtm)



aboutGoods="12" # This data is not there in JSON
gds= GDS()
gds.nature_Of_Cargo_01_01=aboutGoods
ediData.add_segment(gds)


modeOfTransport=""
if(json_data[0]["ModeOfTransport"]=="Sea"):
     modeOfTransport="1"
elif(json_data[0]["ModeOfTransport"]=="Rail"):
     modeOfTransport="2"
elif(json_data[0]["ModeOfTransport"]=="Road"):
     modeOfTransport="3"
elif(json_data[0]["ModeOfTransport"]=="Air"):
     modeOfTransport ="4"   

tdt=TDT()
tdt.transport_stage_code_qualifier_01="20"
tdt.mode_of_transport_03_01=modeOfTransport
ediData.add_segment(tdt)



# ediData.add_segment("DTM",["200",modifyDateTimeFormat(json_data[0]["CargoReadyDate"],"%Y-%m-%dT%H:%M:%SZ","%Y%m%d%H%M%S"),"304"])

dtm1= DTM()

dtm1.dateTime_code_qualifier_01_01="200"
dtm1.dateTime_value_01_02=modifyDateTimeFormat(json_data[0]["CargoReadyDate"],"%Y-%m-%dT%H:%M:%SZ","%Y%m%d%H%M%S")
dtm1.dateTime_Format_01_03="304"
ediData.add_segment(dtm1)




def map_movement_type(movement_type):
    if movement_type == "P2P":
        return "10"
    elif movement_type == "D2D":
        return "27"
    elif movement_type == "D2P":
        return "28"
    elif movement_type == "P2D":
        return "29"
    else:
        return ""

def map_lane_id(lane_id):
    if 'E' in lane_id:
        return '3'
    elif 'P' in lane_id:
        return '1'
    else:
        return ""


tsr1= TSR()

tsr1.contract_and_carriage_condition_Code_01_01 =map_movement_type(json_data[0]["MovementType"])
tsr1.service_requirement_code_02_01=map_lane_id(json_data[0]["LaneId"])
tsr1.nature_of_Cargo_04_01=aboutGoods

ediData.add_segment(tsr1)


def map_lane_id2(lane_id):
    if 'E' in lane_id:
        return 'Economy'
    elif 'P' in lane_id:
        return 'Priority'
    else:
        return ""

if modeOfTransport=="4":
    ftx1=FTX()
    ftx1.text_subject_code_qualifier_01="SSR"
    ftx1.free_text_Value_04_01=map_lane_id2(json_data[0]["LaneId"])
    ediData.add_segment(ftx1)
    
# # count of cargoMeasurement:

cargoQuantityCount=0

for cargo in json_data[0]["CargoMeasurements"]:
   cargoQuantityCount=cargoQuantityCount+int(cargo["Quantity"])


ftx2=FTX()
ftx2.text_subject_code_qualifier_01="PKG"
ftx2.free_text_Value_04_01="NonStackable "+str(cargoQuantityCount)+" Pallet"
ediData.add_segment(ftx2)

def convert_load_type(load_type):
    if load_type == "CYCY":
        return "FCL"
    elif load_type == "CFSCFS":
        return "LCL"
    elif load_type == "LTL":
        return "LTL"
    elif load_type == "FTL":
        return "FTL"
    else:
        return ""

loadType = json_data[0]["LoadType"]

valid_load_types = {"CYCY", "CFSCFS", "LTL", "FTL"}

if loadType in valid_load_types:
    ftx3=FTX()
    ftx3.text_subject_code_qualifier_01="AGK"
    ftx3.free_text_Value_04_01=convert_load_type(loadType)
    ediData.add_segment(ftx3)





# ediData.add_segment("MEA","WT")
# ediData.add_segment("MEA","VOL")
mea1=MEA()
mea1.measurement_attribute_code_01="WT"
ediData.add_segment(mea1)

mea2=MEA()
mea2.measurement_attribute_code_01="VOL"
ediData.add_segment(mea2)


for cargo in json_data[0]["CargoMeasurements"]:
  dat22=pack_type_codeList[cargo["PackType"]]
  mea3=MEA()
  mea3.measurement_attribute_code_01="CT"
  mea3.measurement_unit_code_03_01=dat22
  mea3.measurement_value_03_02=str(int(cargo["Quantity"]))
  mea3.measured_attribute_code_02_01=""
  ediData.add_segment(mea3)




for cargo in json_data[0]["CargoMeasurements"]:
    length=cargo["Length"]["Amount"]/100
    width=cargo["Width"]["Amount"]/100
    height1=cargo["Height"]["Amount"]/100
    dim1=DIM()
    dim1.dimension_qualifier_01="4"
    dim1.measurement_unit_code_02_01="MTR"
    dim1.length_dimension_02_02=length
    dim1.width_dimension_02_03=width
    dim1.height_dimension_02_04=height1
    ediData.add_segment(dim1)
    eqn1=EQN()
    eqn1.number_of_unit_01_01=str(int(cargo["Quantity"]))
    ediData.add_segment(eqn1)


eqd1=EQD()
eqd1.equipment_type_code_qualifier_01="CN"
eqd1.equipment_size_and_type_description_03_04=json_data[0]["VendorBookingEquipments"][0]["ContainerTypeCode"]
ediData.add_segment(eqd1)

eqn2=EQN()
eqn2.number_of_unit_01_01=str(len(json_data[0]["VendorBookingEquipments"]))
ediData.add_segment(eqn2)

cni1=CNI()
cni1.consolidation_item_number_01="1"
cni1.documnet_number_02_01=json_data[0]["BookingReference"]
ediData.add_segment(cni1)

def determine_code(inco_term_code):
    if inco_term_code in ["DAP", "DDP", "DAT", "DPU"]:
        return "1"
    else:
        return "2"

tod1=TOD()
tod1.terms_of_delivery_function_coded_01="6"
tod1.delivery_description_code_03_01=determine_code(json_data[0]["IncoTermCode"])
tod1.code_list_identification_code_03_02="106"
tod1.code_list_responsible_agency_code_03_03="6"
tod1.delivery_term_description_03_04=json_data[0]["IncoTermCode"]
ediData.add_segment(tod1)

loc1=LOC()
loc1.location_function_code_qualifer_01="1"
loc1.location_name_code_02_01=""
loc1.location_name_02_04=json_data[0]["IncoTermNamedPlace"]
ediData.add_segment(loc1)


# ediData.add_segment("RFF",["AHX",json_data[0]["LaneId"]])
rff1= RFF()
rff1.reference_function_code_qualifier_01_01="AHX"
rff1.reference_identifier_01_02=json_data[0]["LaneId"]
ediData.add_segment(rff1)

# ediData.add_segment("NAD","CN",[json_data[0]["ConsigneeNode"]["Code"]],"",split_string(json_data[0]["ConsigneeNode"]["Name"],35),split_string(json_data[0]["ConsigneeNode"]["Address"]["Street"],35),json_data[0]["ConsigneeNode"]["Address"]["City"],"",json_data[0]["ConsigneeNode"]["Address"]["PostalCode"],json_data[0]["ConsigneeNode"]["Address"]["CountryCode"])
nad1= NAD()
nad1.party_function_code_qualifier_01="CN"
nad1.party_identifier_02_01=json_data[0]["ConsigneeNode"]["Code"]

nameList=split_string(json_data[0]["ConsigneeNode"]["Name"],35)
counter=1
for name in nameList:
    if(counter==1):
        nad1.party_name_04_01=name
    elif(counter==2):
        nad1.party_name_04_02=name
    elif(counter==3):
        nad1.party_name_04_03=name
    elif(counter==4):
        nad1.party_name_04_04=name
    elif(counter==5):
        nad1.party_name_04_05=name
    counter=counter+1

counter=1
streetList=split_string(json_data[0]["ConsigneeNode"]["Address"]["Street"],35)
for street in streetList:
    if(counter==1):
        nad1.street_and_number_05_01=street
    elif(counter==2):
        nad1.street_and_number_05_02=street
    elif(counter==3):
        nad1.street_and_number_05_03=street
    elif(counter==4):
        nad1.street_and_number_05_04=street
    counter=counter+1

nad1.city_name_06=json_data[0]["ConsigneeNode"]["Address"]["City"]
nad1.postal_identification_code_08=json_data[0]["ConsigneeNode"]["Address"]["PostalCode"]
nad1.country_name_code_09=json_data[0]["ConsigneeNode"]["Address"]["CountryCode"]
ediData.add_segment(nad1)

# ediData.add_segment("NAD","CZ",[json_data[0]["ShipperNode"]["Code"]],"",split_string(json_data[0]["ShipperNode"]["Name"],35),split_string(json_data[0]["ShipperNode"]["Address"]["Street"],35),json_data[0]["ShipperNode"]["Address"]["City"],"",json_data[0]["ShipperNode"]["Address"]["PostalCode"],json_data[0]["ShipperNode"]["Address"]["CountryCode"])

nad2=NAD()
nad2.party_function_code_qualifier_01="CZ"
nad2.party_identifier_02_01=json_data[0]["ShipperNode"]["Code"]

nameList=split_string(json_data[0]["ShipperNode"]["Name"],35)
counter=1
for name in nameList:
    if(counter==1):
        nad2.party_name_04_01=name
    elif(counter==2):
        nad2.party_name_04_02=name
    elif(counter==3):
        nad2.party_name_04_03=name
    elif(counter==4):
        nad2.party_name_04_04=name
    elif(counter==5):
        nad2.party_name_04_05=name
    counter=counter+1

counter=1
streetList=split_string(json_data[0]["ShipperNode"]["Address"]["Street"],35)
for street in streetList:
    if(counter==1):
        nad2.street_and_number_05_01=street
    elif(counter==2):
        nad2.street_and_number_05_02=street
    elif(counter==3):
        nad2.street_and_number_05_03=street
    elif(counter==4):
        nad2.street_and_number_05_04=street
    counter=counter+1

nad2.city_name_06=json_data[0]["ShipperNode"]["Address"]["City"]
nad2.postal_identification_code_08=json_data[0]["ShipperNode"]["Address"]["PostalCode"]
nad2.country_name_code_09=json_data[0]["ShipperNode"]["Address"]["CountryCode"]
ediData.add_segment(nad2)


# # Looping for Multiple Orders and Items in it.
gidCounter=0
for bookingOrder in json_data[0]["VendorBookingOrders"]:
    for bookingItem in bookingOrder["VendorBookingItems"]:
        print(bookingItem["Description"])
        gidCounter=gidCounter+1
        packTYpeCode=pack_type_codeList[bookingItem["PackType"]]
        # GID Mapping
        gid1=GID()
        gid1.goods_item_number_01=gidCounter
        gid1.number_of_packages_02_01=str(int(bookingItem["Quantity"]))
        gid1.pack_type_description_code_02_02=packTYpeCode
        gid1.type_of_package_02_05=packTYpeCode
        ediData.add_segment(gid1)
        # LOC 9 mapping
        loc2=LOC()
        loc2.location_function_code_qualifer_01="9"
        loc2.location_name_code_02_01=json_data[0]["PolCode"]
        loc2.location_name_02_04=json_data[0]["PolName"]
        loc2.relation_coded_05="1"
        ediData.add_segment(loc2)
        # LOC 12 mapping
        loc3=LOC()
        loc3.location_function_code_qualifer_01="12"
        loc3.location_name_code_02_01=json_data[0]["PodCode"]
        loc3.location_name_02_04=json_data[0]["PodName"]
        loc3.relation_coded_05="2"
        ediData.add_segment(loc3)
        # GIN mapping
        gin1=GIN()
        gin1.object_identification_code_qualifier_01="PN"
        gin1.object_identifier_02_01=bookingItem["ItemCode"]
        ediData.add_segment(gin1)
        gin2=GIN()  
        gin2.object_identification_code_qualifier_01="BN"
        gin2.object_identifier_02_01=bookingOrder["Identifier"]
        ediData.add_segment(gin2)
        # FTX Mapping
        ftx4=FTX()
        ftx4.text_subject_code_qualifier_01="AAA"
        ftx4.free_text_Value_04_01=bookingItem["Description"]
        ediData.add_segment(ftx4)
        # NAD Loop mapping
        nad1= NAD()
        nad1.party_function_code_qualifier_01="UC"
        nad1.party_identifier_02_01=json_data[0]["ConsigneeNode"]["Code"]

        nameList=split_string(json_data[0]["ConsigneeNode"]["Name"],35)
        counter=1
        for name in nameList:
            if(counter==1):
                nad1.party_name_04_01=name
            elif(counter==2):
                nad1.party_name_04_02=name
            elif(counter==3):
                nad1.party_name_04_03=name
            elif(counter==4):
                nad1.party_name_04_04=name
            elif(counter==5):
                nad1.party_name_04_05=name
            counter=counter+1

        counter=1
        streetList=split_string(json_data[0]["ConsigneeNode"]["Address"]["Street"],35)
        for street in streetList:
            if(counter==1):
                nad1.street_and_number_05_01=street
            elif(counter==2):
                nad1.street_and_number_05_02=street
            elif(counter==3):
                nad1.street_and_number_05_03=street
            elif(counter==4):
                nad1.street_and_number_05_04=street
            counter=counter+1

        nad1.city_name_06=json_data[0]["ConsigneeNode"]["Address"]["City"]
        nad1.postal_identification_code_08=json_data[0]["ConsigneeNode"]["Address"]["PostalCode"]
        nad1.country_name_code_09=json_data[0]["ConsigneeNode"]["Address"]["CountryCode"]
        ediData.add_segment(nad1)

        # ediData.add_segment("NAD","CZ",[json_data[0]["ShipperNode"]["Code"]],"",split_string(json_data[0]["ShipperNode"]["Name"],35),split_string(json_data[0]["ShipperNode"]["Address"]["Street"],35),json_data[0]["ShipperNode"]["Address"]["City"],"",json_data[0]["ShipperNode"]["Address"]["PostalCode"],json_data[0]["ShipperNode"]["Address"]["CountryCode"])

        nad2=NAD()
        nad2.party_function_code_qualifier_01="OS"
        nad2.party_identifier_02_01=json_data[0]["ShipperNode"]["Code"]

        nameList=split_string(json_data[0]["ShipperNode"]["Name"],35)
        counter=1
        for name in nameList:
            if(counter==1):
                nad2.party_name_04_01=name
            elif(counter==2):
                nad2.party_name_04_02=name
            elif(counter==3):
                nad2.party_name_04_03=name
            elif(counter==4):
                nad2.party_name_04_04=name
            elif(counter==5):
                nad2.party_name_04_05=name
            counter=counter+1

        counter=1
        streetList=split_string(json_data[0]["ShipperNode"]["Address"]["Street"],35)
        for street in streetList:
            if(counter==1):
                nad2.street_and_number_05_01=street
            elif(counter==2):
                nad2.street_and_number_05_02=street
            elif(counter==3):
                nad2.street_and_number_05_03=street
            elif(counter==4):
                nad2.street_and_number_05_04=street
            counter=counter+1

        nad2.city_name_06=json_data[0]["ShipperNode"]["Address"]["City"]
        nad2.postal_identification_code_08=json_data[0]["ShipperNode"]["Address"]["PostalCode"]
        nad2.country_name_code_09=json_data[0]["ShipperNode"]["Address"]["CountryCode"]
        ediData.add_segment(nad2)
        # DTM mapping
        dtm2=DTM()
        dtm2.dateTime_code_qualifier_01_01="2"
        dtm2.dateTime_value_01_02=modifyDateTimeFormat(bookingItem["IntoDcDate"],"%Y-%m-%dT%H:%M:%SZ","%Y%m%d%H%M%S")
        dtm2.dateTime_Format_01_03="304"
        ediData.add_segment(dtm2)
        # MEA mapping
        if str(bookingItem["Weight"]["Amount"])!="0.0":
            mea4=MEA()
            mea4.measurement_attribute_code_01="WT"
            mea4.measured_attribute_code_02_01="ABS"
            mea4.measurement_unit_code_03_01="KGM"
            mea4.measurement_value_03_02=str(bookingItem["Weight"]["Amount"])
            ediData.add_segment(mea4)
        # RFF mapping
        rff2=RFF()
        rff2.reference_function_code_qualifier_01_01="ON"
        rff2.reference_identifier_01_02=bookingOrder["OrderNumber"]
        ediData.add_segment(rff2)
        #PCI Mapping
        pci1=PCI()
        pci1.shipping_marks_02_01=json_data[0]["MarksAndNumbers"]
        ediData.add_segment(pci1)





# #----------------------------------------------------------------Mapping Logic End----------------------------------------------------------------  

ediData = ediData.create_edi()
print(ediData)
write_data_to_file(ediData,"C:\\Users\\rakro\\Desktop\\EDI Template Class Based\\Output2EDI.edi")


print("Mapping Done !!!!!!!!!")
print("ThankYou")


#path To lib  :  pydifact in c:\users\rakro\appdata\local\programs\python\python311\lib\site-packages (0.1.6)
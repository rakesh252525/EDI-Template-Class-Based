import datetime

# Main Class to create edi Data

class EDIData:
    def __init__(self,message_type,version,release,senderId,reciverId):
        self.segments = []
        self.message_type = message_type
        self.version = version
        self.release = release
        self.senderId = senderId
        self.reciverId=reciverId
       


    def add_segment(self, segment):
        self.segments.append(segment)
    
    def create_edi(self):
        edi_data = ""

        # UNB segment
        unb_segment = "UNB+UNOC:1+{}:01:ZZZ+{}:16:ZZZ+{:%Y%m%d}:{:%H%M}+8479++++1'"
        edi_data += unb_segment.format(self.senderId,self.reciverId,datetime.datetime.now(), datetime.datetime.now())

        # UNH segment
        unh_segment = "UNH+00000000008479+{message_type}:{version}:{release}+D'"
        edi_data += unh_segment.format(message_type=self.message_type, version=self.version, release=self.release)

        # Add segments and elements

        for segment in self.segments:
            edi_data= edi_data+segment.to_edifact()

        # UNT segment
        unt_segment = "UNT+{segment_count}+00000000008479'"
        edi_data += unt_segment.format(segment_count=len(self.segments) + 2)

        # UNZ segment
        unz_segment = "UNZ+1+8479'"
        edi_data += unz_segment

        return edi_data



class BGM:
    def __init__(self):
        self.document_name_code_01_01 = None
        self.document_number_02_01 = None
        self.message_function_code_03 = None

    def to_edifact(self):
        edifact_data = f"BGM+{self.document_name_code_01_01}+{self.document_number_02_01}+{self.message_function_code_03}'"
        return edifact_data

class DTM:
    def __init__(self):
        self.dateTime_code_qualifier_01_01=None
        self.dateTime_value_01_02=None
        self.dateTime_Format_01_03=None

    def to_edifact(self):
        edifact_data = f"DTM+{self.dateTime_code_qualifier_01_01}:{self.dateTime_value_01_02}:{self.dateTime_Format_01_03}'"
        return edifact_data    


class GDS:
    def __init__(self):
        self.nature_Of_Cargo_01_01=None

    def to_edifact(self):
        edifact_data = f"GDS+{self.nature_Of_Cargo_01_01}'"
        return edifact_data

class TDT:
    def __init__(self):
        self.transport_stage_code_qualifier_01=None
        self.mode_of_transport_03_01=None

    def to_edifact(self):
        edifact_data = f"TDT+{self.transport_stage_code_qualifier_01}++{self.mode_of_transport_03_01}'"
        return edifact_data

class TSR:
    def __init__(self):
        self.contract_and_carriage_condition_Code_01_01=None
        self.service_requirement_code_02_01=None
        self.nature_of_Cargo_04_01=None
    def to_edifact(self):
        edifact_data = f"TSR+{self.contract_and_carriage_condition_Code_01_01}+{self.service_requirement_code_02_01}++{self.nature_of_Cargo_04_01}'"
        return edifact_data

class FTX:
    def __init__(self):
        self.text_subject_code_qualifier_01 = None
        self.free_text_Value_04_01 = None

    def to_edifact(self):
        edifact_data = f"FTX+{self.text_subject_code_qualifier_01}+++{self.free_text_Value_04_01}'"
        return edifact_data


class MEA:
    def __init__(self):
        self.measurement_attribute_code_01 = None
        self.measured_attribute_code_02_01 = None
        self.measurement_unit_code_03_01 = None
        self.measurement_value_03_02 = None

    def to_edifact(self):
        edifact_data = f"MEA+{self.measurement_attribute_code_01}+{self.measured_attribute_code_02_01}+{self.measurement_unit_code_03_01}:{self.measurement_value_03_02}'"
        return edifact_data
    
class DIM:
    def __init__(self):
        self.dimension_qualifier_01 = None
        self.measurement_unit_code_02_01 = None
        self.length_dimension_02_02 = None
        self.width_dimension_02_03 = None
        self.height_dimension_02_04 = None

    def to_edifact(self):
        edifact_data = f"DIM+{self.dimension_qualifier_01}+{self.measurement_unit_code_02_01}:{self.length_dimension_02_02}:{self.width_dimension_02_03}:{self.height_dimension_02_04}'"
        return edifact_data


class EQN:
    def __init__(self):
        self.number_of_unit_01_01= None

    def to_edifact(self):
        edifact_data = f"EQN+{self.number_of_unit_01_01}'"
        return edifact_data


class EQD:
    def __init__(self):
        self.equipment_type_code_qualifier_01= None
        self.equipment_size_and_type_description_03_04= None
    def to_edifact(self):
        edifact_data = f"EQD+{self.equipment_type_code_qualifier_01}++:::{self.equipment_size_and_type_description_03_04}'"
        return edifact_data

class CNI:
    def __init__(self):
        self.consolidation_item_number_01 = None
        self.documnet_number_02_01=None
    def to_edifact(self):
        edifact_data = f"CNI+{self.consolidation_item_number_01}+{self.documnet_number_02_01}'"
        return edifact_data
    
class TOD:
    def __init__(self):
        self.terms_of_delivery_function_coded_01=None
        self.delivery_description_code_03_01=None
        self.code_list_identification_code_03_02=None
        self.code_list_responsible_agency_code_03_03=None
        self.delivery_term_description_03_04=None
    def to_edifact(self):
        edifact_data = f"TOD+{self.terms_of_delivery_function_coded_01}++{self.delivery_description_code_03_01}:{self.code_list_identification_code_03_02}:{self.code_list_responsible_agency_code_03_03}:{self.delivery_term_description_03_04}'"
        return edifact_data
class LOC:
    def __init__(self):
        self.location_function_code_qualifer_01 = None
        self.location_name_code_02_01 = None
        self.location_name_02_04 = None
        self.relation_coded_05 = None
    def to_edifact(self):
        edifact_data = f"LOC+{self.location_function_code_qualifer_01}+{self.location_name_code_02_01}:::{self.location_name_02_04}"
        if self.relation_coded_05!=None:
            edifact_data=edifact_data+f"+++{self.relation_coded_05}'"
        else:
            edifact_data=edifact_data+"'"
        return edifact_data


class RFF:
    def __init__(self):
        self.reference_function_code_qualifier_01_01 = None
        self.reference_identifier_01_02 = None
    
    def to_edifact(self):
        edifact_data = f"RFF+{self.reference_function_code_qualifier_01_01}:{self.reference_identifier_01_02}'"
        return edifact_data


class NAD:
    def __init__(self):
        self.party_function_code_qualifier_01 = None
        self.party_identifier_02_01 = None
        self.party_name_04_01 = None
        self.party_name_04_02 = None
        self.party_name_04_03 = None
        self.party_name_04_04 = None
        self.party_name_04_05 = None
        self.street_and_number_05_01 = None
        self.street_and_number_05_02 = None
        self.street_and_number_05_03 = None
        self.street_and_number_05_04 = None
        self.city_name_06 = None
        self.postal_identification_code_08 = None
        self.country_name_code_09 = None
    
    def to_edifact(self):
        edifact_data = f"NAD+{self.party_function_code_qualifier_01}+{self.party_identifier_02_01}++{self.party_name_04_01}"
        if(self.party_name_04_02!=None):
            edifact_data=edifact_data+f":{self.party_name_04_02}"
        if(self.party_name_04_03!=None):
            edifact_data=edifact_data+f":{self.party_name_04_03}"
        if(self.party_name_04_04!=None):
            edifact_data=edifact_data+f":{self.party_name_04_04}"
        if(self.party_name_04_05!=None):
            edifact_data=edifact_data+f":{self.party_name_04_05}"
        edifact_data=edifact_data+f"+{self.street_and_number_05_01}"
        if(self.street_and_number_05_02!=None):
            edifact_data=edifact_data+f":{self.street_and_number_05_02}"
        if(self.street_and_number_05_03!=None):
            edifact_data=edifact_data+f":{self.street_and_number_05_03}"
        if(self.street_and_number_05_04!=None):
            edifact_data=edifact_data+f":{self.street_and_number_05_04}"
        edifact_data=edifact_data+f"+{self.city_name_06}++{self.postal_identification_code_08}+{self.country_name_code_09}'"
           
        return edifact_data

class GID:
    def __init__(self):
        self.goods_item_number_01 = None
        self.number_of_packages_02_01 = None
        self.pack_type_description_code_02_02 = None
        self.type_of_package_02_05 = None

    def to_edifact(self):
        edifact_data = f"GID+{self.goods_item_number_01}+{self.number_of_packages_02_01}:{self.pack_type_description_code_02_02}:::{self.type_of_package_02_05}'"
        return edifact_data
    
class GIN:
    def __init__(self):
        self.object_identification_code_qualifier_01 = None
        self.object_identifier_02_01 = None
    def to_edifact(self):
        edifact_data = f"GIN+{self.object_identification_code_qualifier_01}+{self.object_identifier_02_01}'"
        return edifact_data



class PCI:
    def __init__(self):
        self.shipping_marks_02_01 = None

    def to_edifact(self):
        edifact_data = f"PCI++{self.shipping_marks_02_01}'"
        return edifact_data
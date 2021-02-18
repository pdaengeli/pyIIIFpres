
from . import plus
import json
global BASE_URL
BASE_URL = "https://iiif.io/api/cookbook/recipe/0009-book-1/"

class Required(object):
    """
    This is not an IIIF object but a class used by this software to identify required fields.
    This is equivalente to MUST statement in the guideline.
    """
    def __init__(self,description=None):
        self.problem_description = description
    def __repr__(self): 
        return 'Required attribute:%s' %self.problem_description

class Suggested(object):
    """
    This is not an IIIF object but a class used by this software to identify required fields.
    This is equivalente to SHOULD statement in the guideline.
    """
    def __init__(self,description=None):
        self.suggested = description
    def __repr__(self): 
        return 'Suggested attribute:%s' %self.suggested

# Let's group all the common arguments across the differnet types of collection

def unused(attr):
    """
    This function check if an attribute is not set (has no value in it).
    """
    if isinstance(attr, Required) or isinstance(attr, Suggested) or attr is None:
        return True
    else:
        return False

class CoreAttributes(object):
    """
    Core attributes are the attributes that are with all the major
    classes/containers of IIIF namely: Collection, Manifest, Canvas, Range and
    Annotation Page, Annotation and Content and also in the minor classes such 
    as SeeAlso and partOf.

    ID an type attributes are required. The other might vary. 
    """
    def __init__(self):
        self.id = Required("A %s should have the ID property with at least one item." %self.__class__.__name__)
        self.type = self.__class__.__name__
        # These might be suggested or may be used if needed.
        self.label = None
    
    def set_id(self,objid=None,extendbase_url=None):
        """
        IIIF : The id property identifies this object with the URL at which it is available online.
        """
        if extendbase_url:
            if objid:
                ValueError("Set id using extendbase_url or objid not both.")
            if isinstance(extendbase_url,str):
                self.id = "/".join((BASE_URL,extendbase_url))
            if isinstance(extendbase_url,list):
                extendbase_url.insert(0,BASE_URL )
                self.id = "/".join(extendbase_url)
        elif objid is None:
            objid = BASE_URL
        else:
            self.id = objid
   
    def set_type(self):
        print("The type property must be kept %s." %self.__class__.__name__)
    
    def add_label(self,language,text):
        """
        IIIF : A human readable label, name or title. The label property is intended to be displayed 
        as a short, textual surrogate for the resource if a human needs to make a distinction 
        between it and similar resources, for example between objects, pages, or options for 
        a choice of images to display. The label property can be fully internationalized, and 
        each language can have multiple values.
        """
        if unused(self.label):
            self.label = {}
        self.label[language] = [text]

    def json_dumps(self,dumps_errors=False):
        context = "http://iiif.io/api/presentation/3/context.json"
        def serializerwitherrors(obj):
            return {k: v for k, v in obj.__dict__.items() if v is not None}
        def serializer(obj):
            return {k: v for k, v in obj.__dict__.items() if not unused(v)}
        if dumps_errors:
            res = json.dumps(self,default = serializerwitherrors,indent=1)
        else:
            res = json.dumps(self,default = serializer,indent=1)
        # little hack for fixing context first 3 chrs "{\n"
        res = "".join(('{\n "@context" : "%s", \n '%context,res[3:]))
        return res

    def json_save(self,filename,save_errors=False):
        with open(filename,'w') as f:
            f.write(self.json_dumps(dumps_errors=save_errors))

    def show_errors(self):
        return print(self.json_dumps(dumps_errors=True))

    def __repr__(self) -> str:
        return self.json_dumps()


class seeAlso(CoreAttributes):
    """
    IIF: A machine-readable resource such as an XML or RDF description that is related to the
    current resource that has the seeAlso property. Properties of the resource should be given 
    to help the client select between multiple descriptions (if provided), and to make 
    appropriate use of the document. If the relationship between the resource and the document 
    needs to be more specific, then the document should include that relationship rather than 
    the IIIF resource. Other IIIF resources are also valid targets for seeAlso, for example to 
    link to a Manifest that describes a related object. The URI of the document must identify a
    single representation of the data in a particular format. For example, if the same data 
    exists in JSON and XML, then separate resources should be added for each representation, 
    with distinct id and format properties.
    """
    def __init__(self):
        super(seeAlso, self).__init__()
        self.format = Suggested()
        self.profile = Suggested()

    def set_type(self,datatype):
        #TODO: add check
        self.type = datatype
    
    def set_profile(self,profile):
        #TODO: add check
        self.profile = profile
    
    def set_format(self,format):
        #TODO: add check
        self.format = format


class partOf(CoreAttributes): 
    """
    A containing resource that includes the resource that has the partOf property. 
    When a client encounters the partOf property, it might retrieve the referenced 
    containing resource, if it is not embedded in the current representation, in order 
    to contribute to the processing of the contained resource. For example, the partOf 
    property on a Canvas can be used to reference an external Manifest in order to 
    enable the discovery of further relevant information. Similarly, a Manifest can 
    reference a containing Collection using partOf to aid in navigation.
    """
    def __init__(self):
        super(partOf,self).__init__()
    
    def set_type(self,type):
        self.type = type

    def set_id(self, objid):
        self.id = objid


class supplementary(CoreAttributes):
    """
    A link from this Range to an Annotation Collection that includes the supplementing Annotations 
    of content resources for the Range. Clients might use this to present additional content to the 
    user from a different Canvas when interacting with the Range, or to jump to the next part of the 
    Range within the same Canvas. For example, the Range might represent a newspaper article that spans
    non-sequential pages, and then uses the supplementary property to reference an Annotation Collection
    that consists of the Annotations that record the text, split into Annotation Pages per newspaper page. 
    Alternatively, the Range might represent the parts of a manuscript that have been transcribed or 
    translated, when there are other parts that have yet to be worked on. The Annotation Collection would
    be the Annotations that transcribe or translate, respectively.
    """
    def __init__(self):
        super(supplementary,self).__init__()
        self.type = "Supplementary"
    
    def set_type(self):
        print("type must be AnnotationCollection")


class body(CoreAttributes,plus.HeightWidthDuration):
    def __init__(self):
        super(body,self).__init__()
        self.type = Required("The type of the content resource must be included, and should be taken from the table listed under the definition of type.")
        self.format = Suggested("The format of the resource should be included and, if so, should be the media type that is returned when the resource is dereferenced.")
        self.profile = Suggested("The profile of the resource, if it has one, should also be included.")
        self.service = None
    
    def set_type(self,mytype):
        self.type = mytype
    
    def set_format(self,format):
        self.format = format
    
    def add_service(self,service):
        if unused(self.service):
            self.service = []
        self.service.append(service)

class CommonAttributes(CoreAttributes):
    """
    Common attributes are the attributes that are in common with all the major
    classes/container of IIIF namely: Collection, Manifest, Canvas, Range and
    Annotation Page, Annotation and Content.

    ID an type attributes are required. The other might vary. 
    """
    def __init__(self):
        super(CommonAttributes, self).__init__()
        self.metadata = None
        self.summary = None
        self.requiredStatement = None
        self.rights = None
        # https://iiif.io/api/presentation/3.0/#thumbnail
        self.thumbnail = None
        self.behavior = None
        self.seeAlso = None
        self.service = None
        self.hompage = None
        self.rendering = None
        self.partOf = None
    
    def add_metadata(self,label=None,value=None,language_l=None,
                     language_v=None,entry=None):
        """
        An ordered list of descriptions to be displayed to the user when they interact
        with the resource, given as pairs of human readable label and value entries. 
        The content of these entries is intended for presentation only; descriptive 
        semantics should not be inferred. An entry might be used to convey 
        information about the creation of the object, a physical description, 
        ownership information, or other purposes.
        """
        if unused(self.metadata):
            self.metadata = []
        arggr = [label,value,language_l,language_v]
        if any(elem is not None for elem in arggr ) and entry is not None:
            ValueError("Either use entry arguments or a combination of other arguments, NOT both.")
        if entry is None:
            entry = {"label":{language_l:[label]},
                    "value":{language_l:[value]}}
        self.metadata.append(entry)

    def add_summary(self,text,language):
        """
        An ordered list of descriptions to be displayed to the user when they interact
        with the resource, given as pairs of human readable label and value entries. 
        The content of these entries is intended for presentation only; descriptive 
        semantics should not be inferred. An entry might be used to convey 
        information about the creation of the object, a physical description, 
        ownership information, or other purposes.
        """
        if unused(self.summary):
            self.summary = {}
        self.summary[language] = [text]
    
    def add_requiredStatement(self,label,value,language):

        if unused(self.requiredStatement):
            self.requiredStatement = {}
        self.requiredStatement["label"] = {language:[label]}
        self.requiredStatement["value"] = {language:[value]}
    
    def add_requiredStatement(self,label=None,value=None,language_l=None,
                     language_v=None,entry=None):
        """
        IIIF: Text that must be displayed when the resource is displayed or used. 
        For example, the requiredStatement property could be used to present 
        copyright or ownership statements, an acknowledgement of the owning and/or
        publishing institution, or any other text that the publishing organization 
        deems critical to display to the user. Given the wide variation of potential 
        client user interfaces, it will not always be possible to display this 
        statement to the user in the client’s initial state. If initially hidden, 
        clients must make the method of revealing it as obvious as possible.
        """
        if unused(self.requiredStatement):
            self.requiredStatement = {}
        arggr = [label,value,language_l,language_v]
        if any(elem is not None for elem in arggr ) and entry is not None:
            ValueError("Either use entry arguments or a combination of other arguments, NOT both.")
        if entry is None:
            entry = {"label":{language_l:[label]},
                    "value":{language_l:[value]}}
        self.requiredStatement = entry

    def set_rights(self,rights):
        """
        A string that identifies a license or rights statement that applies to the 
        content of the resource, such as the JSON of a Manifest or the pixels of an
        image. The value must be drawn from the set of Creative Commons license URIs,
        the RightsStatements.org rights statement URIs, or those added via the 
        extension mechanism. The inclusion of this property is informative, and for
        example could be used to display an icon representing the rights assertions.
        
        Not sure if it is suggested or mandatory.
        """
        #TODO: CHECK IF IT IS A VALID URL
        self.rights =  rights

    def add_thumbnail(self,obj):
        """
        https://iiif.io/api/presentation/3.0/#thumbnail
        A content resource, such as a small image or short audio clip, that represents the 
        resource that has the thumbnail property. A resource may have multiple thumbnail resources
         that have the same or different type and format.

        The value must be an array of JSON objects, each of which must have the id and type properties, 
        and should have the format property. Images and videos should have the width and height properties,
        and time-based media should have the duration property. It is recommended that a IIIF Image API 
        service be available for images to enable manipulations such as resizing.
        """
        if unused(self.thumbnail):
            self.thumbnail = []
        self.thumbnail.append(obj)

    def add_behavior(self,behavior):
        """
        """
        #TODO: CHECK IF ALLOWED
        if unused(self.behavior):
            self.behavior = []
        self.behavior.append(behavior)
    
    def add_hompage(self,hompage):
        """
        """
        #TODO: CHECK IF ALLOWED
        if unused(self.hompage):
            self.hompage = []
        self.hompage.append(hompage)
    
    def add_seeAlso(self,seeAlso):
        """
        """
        #TODO: CHECK IF ALLOWED
        if unused(self.seeAlso):
            self.seeAlso = []
        self.seeAlso.append(seeAlso)

    def add_partOf(self,partOf):
        """
        """
        #TODO: CHECK IF ALLOWED
        if unused(self.partOf):
            self.partOf = []
        self.partOf.append(partOf)
    
    def add_rendering(self,rendering):
        """
        """
        #TODO: CHECK IF ALLOWED
        if unused(self.rendering):
            self.rendering = []
        self.rendering.append(rendering)
        

class service(CommonAttributes):
    """https://iiif.io/api/presentation/3.0/#service
    A service that the client might interact with directly and 
    gain additional information or functionality for using the 
    resource that has the service property, such as from an 
    Image to the base URI of an associated IIIF Image API 
    service. The service resource should have additional 
    information associated with it in order to allow the 
    client to determine how to make appropriate use of it. 
    Please see the Service Registry document for the details 
    of currently known service types.

    The value must be an array of JSON objects. Each object 
    will have properties depending on the service’s definition,
     but must have either the id or @id and type or @type 
     properties. Each object should have a profile property.

    Any resource type may have the service property with at 
    least one item.
    Clients may process service on any resource type, and 
    should process the IIIF Image API service.

    """
    def __init__(self):
        super(service,self).__init__()
        self.profile = Suggested("Each object should have a profile property.")
        self.service = None


    def set_type(self,mytype):
        values = [
            "ImageService",
            "SearchService",
            "AutoCompleteService",
            "AuthCookieService",
            "AuthTokenService",
            "AuthLogoutService"]
        if mytype in values:
            self.type = mytype
        else:
            ValueError("mytype not right must be one of these value %s" %",".join(values))
    
    def set_type(self,mtype):
        self.type = mtype
        
    def set_profile(self,profile):
        self.profile = profile
    
    def add_service(self,service):
        if unused(self.service):
            self.service = []
        self.service.append(service)

class Annotation(CommonAttributes):
    """

    https://iiif.io/api/presentation/3.0/#56-annotation 
    Annotations follow the Web Annotation data model. The description provided here is a summary 
    plus any IIIF specific requirements. The W3C standard is the official documentation.

    Annotations must have their own HTTP(S) URIs, conveyed in the id property. The JSON-LD 
    description of the Annotation should be returned if the URI is dereferenced, according to 
    the Web Annotation Protocol.

    When Annotations are used to associate content resources with a Canvas, the content resource
    is linked in the body of the Annotation. The URI of the Canvas must be repeated in the target
    property of the Annotation, or the source property of a Specific Resource used in the target 
    property.

    Note that the Web Annotation data model defines different patterns for the value property, 
    when used within an Annotation. The value of a Textual Body or a Fragment Selector, for example,
    are strings rather than JSON objects with languages and values. Care must be taken to use the 
    correct string form in these cases.

    Additional features of the Web Annotation data model may also be used, such as selecting a 
    segment of the Canvas or content resource, or embedding the comment or transcription within 
    the Annotation. The use of these advanced features sometimes results in situations where the 
    target is not a content resource, but instead a SpecificResource, a Choice, or other 
    non-content object. Implementations should check the type of the resource and not assume that 
    it is always content to be rendered.
    """
    #https://iiif.io/api/presentation/3.0/#56-annotation 
    def __init__(self,target):
        super(CommonAttributes, self).__init__()
        self.motivation = None
        self.body = body()
        self.target = target
          
    def set_motivation(self,motivation):
        """
        https://iiif.io/api/presentation/3.0/#values-for-motivation
        Values for motivation
        This specification defines two values for the Web Annotation property of 
        motivation, or purpose when used on a Specific Resource or Textual 
        Body.

        While any resource may be the target of an Annotation, this 
        specification defines only motivations for Annotations that 
        target Canvases. These motivations allow clients to determine 
        how the Annotation should be rendered, by distinguishing between 
        Annotations that provide the content of the Canvas, from ones with
        externally defined motivations which are typically comments about
        the Canvas.

        Additional motivations may be added to the Annotation to further 
        clarify the intent, drawn from extensions or other sources. 
        Clients must ignore motivation values that they do not understand.
        Other motivation values given in the Web Annotation specification 
        should be used where appropriate, and examples are given in the 
        Presentation API Cookbook.

        Value	Description
        painting	Resources associated with a Canvas by an Annotation
        that has the motivation value painting must be presented to the 
        user as the representation of the Canvas. The content can be 
        thought of as being of the Canvas. The use of this motivation 
        with target resources other than Canvases is undefined. 
        For example, an Annotation that has the motivation value
        painting, a body of an Image and the target of the Canvas is
        an instruction to present that Image as (part of) the visual
        representation of the Canvas. Similarly, a textual body is 
        to be presented as (part of) the visual representation of 
        the Canvas and not positioned in some other part of the 
        user interface.

        supplementing	Resources associated with a Canvas by an 
        Annotation that has the motivation value supplementing may 
        be presented to the user as part of the representation of t
        he Canvas, or may be presented in a different part of the 
        user interface. The content can be thought of as being from 
        the Canvas. The use of this motivation with target resources 
        other than Canvases is undefined. For example, an Annotation 
        that has the motivation value supplementing, a body of an 
        Image and the target of part of the Canvas is an instruction
        to present that Image to the user either in the Canvas’s 
        rendering area or somewhere associated with it, and could be
        used to present an easier to read representation of a diagram.
        Similarly, a textual body is to be presented either in the
        targeted region of the Canvas or otherwise associated with it,
        and might be OCR, a manual transcription or a translation of
        handwritten text, or captions for what is
        """

        motivations = ["painting","supplementing"]
        if motivation not in motivations:
            pass #TODO:warning
        self.motivation = motivation


class AnnotationPage(CommonAttributes):
    """
 
    """
    def __init__(self):
        super(AnnotationPage, self).__init__()
        self.items = Suggested()
        self.annotations = None

    def add_item(self,item):
        if unused(self.items):
            self.items = []
        self.items.append(item)

class Canvas(CommonAttributes):
    """
    https://iiif.io/api/presentation/3.0/#53-canvas
    The Canvas represents an individual page or view and acts as a central point for assembling the
    different content resources that make up the display. Canvases must be identified by a URI and it 
    must be an HTTP(S) URI.
    """
    def __init__(self):
        super(Canvas, self).__init__()
        self.height = Required()
        self.width = Required()
        self.items = Suggested()
        self.annotations = None
    
    def set_width(self,width:int):
        self.width = width
    
    def set_height(self,height:int):
        self.height = height
    
    def set_hightwidth(self,height:int,width:int):
        self.set_width(width)
        self.set_height(height)

    def add_item(self,item):
        if unused(self.items):
            self.items = []
        self.items.append(item)
    
    def add_annotation(self,annotation):
        if unused(self.annotations):
            self.annotations = []
        self.annotations.append(annotation)

class Manifest(CommonAttributes,plus.ViewingDirection,plus.navDate):
    """
    The Manifest resource typically represents a single object 
    and any intellectual work or works embodied within that 
    object. In particular it includes descriptive, rights and 
    linking information for the object. The Manifest embeds 
    the Canvases that should be rendered as views of the object 
    and contains sufficient information for the client to 
    initialize itself and begin to display something quickly to
     the user.

    The identifier in id must be able to be dereferenced to 
    retrieve the JSON description of the Manifest, and thus 
    must use the HTTP(S) URI scheme.

    The Manifest must have an items property, which is an array
    of JSON-LD objects. Each object is a Canvas, with 
    requirements as described in the next section.
    The Manifest may also have a structures property listing 
    one or more Ranges which describe additional structure of 
    the content, such as might be rendered as a table of
    contents. The Manifest may have an annotations property, 
    which includes Annotation Page resources where the 
    Annotations have the Manifest as their target. 
    These will typically be comment style Annotations,
    and must not have painting as their motivation.
    """
    def __init__(self):
        super(Manifest, self).__init__()
        self.start = None
        self.services = None
        self.items = Required()
        self.annotations = None

    def add_item(self,item):
        if unused(self.items):
            self.items = []
        self.items.append(item)
    
    def add_start(self,start):
        if unused(self.start):
            self.start = []
        self.start.append(start)
    
    def add_services(self,services=None):
        if unused(self.services):
            self.services = []
        self.services.append(services)
    
    def add_annotation(self,annotation):
        if unused(self.annotation):
            self.annotation = []
        self.start.append(annotation)
        
        

class Collection(CommonAttributes):
    def __init__(self):
        super(Collection, self).__init__()
        self.services = None
        self.annotations = None
        self.items = Required()
    
    def add_services(self,services=None):
        if unused(self.services):
            self.services = []
        self.services.append(services)
    
    def add_annotation(self,annotation):
        if unused(self.annotation):
            self.annotation = []
        self.start.append(annotation)
    
    def add_item(self,item):
        if unused(self.items):
            self.items = []
        self.items.append(item)


class Range(CommonAttributes):
    def __init__(self):
        super(Range, self).__init__()
        self.annotations = None
        self.items = Required()
        self.supplementaries = None 
    
    def add_annotation(self,annotation):
        if unused(self.annotation):
            self.annotation = []
        self.start.append(annotation)
    
    def add_item(self,item):
        if unused(self.items):
            self.items = []
        self.items.append(item)
    
    def add_start(self,start):
        if unused(self.start):
            self.start = []
        self.start.append(start)

    def add_supplementary(self,supplementary):
        if unused(self.supplementary):
            self.supplementary = []
        self.start.append(supplementary)

class thumbnail(CoreAttributes,plus.HeightWidthDuration):
    def __init__(self):
        super(thumbnail, self).__init__()
        self.service = None

    def set_type(self,mtype):
        self.type = mtype

    def set_format(self,format):
        self.format = format
    
    def add_service(self,service):
        if unused(self.service):
            self.service = []
        self.service.append(service)


class provider(CoreAttributes):
    """
    IIIF: An organization or person that contributed to providing the content of the resource. 
    Clients can then display this information to the user to acknowledge the provider’s contributions. 
    This differs from the requiredStatement property, in that the data is structured, allowing 
    the client to do more than just present text but instead have richer information about the 
    people and organizations to use in different interfaces.

      "provider": [
    {
      "id": "https://example.org/about",
      "type": "Agent",
      "label": { "en": [ "Example Organization" ] },
      "homepage": [
        {
          "id": "https://example.org/",
          "type": "Text",
          "label": { "en": [ "Example Organization Homepage" ] },
          "format": "text/html"
        }
      ],
      "logo": [
        {
          "id": "https://example.org/images/logo.png",
          "type": "Image",
          "format": "image/png",
          "height": 100,
          "width": 120
        }
      ],
      "seeAlso": [
        {
          "id": "https://data.example.org/about/us.jsonld",
          "type": "Dataset",
          "format": "application/ld+json",
          "profile": "https://schema.org/"
        }
      ]
    }
    ]
    """
    def __init__(self):
        super(provider, self).__init__()
        self.context = None
        self.type = "Agent"
        self.items = []
        self.hompage = Suggested()
        self.logo = Suggested()
        self.seeAlso = None 

    def set_type(self):
        print("The type property must be kept Agent.")
    
    def add_logo(self,logo):
        if unused(self.logo):
            self.logo = []
        self.logo.append(logo)

    def add_hompage(self,hompage):
        if unused(self.hompage):
            self.hompage = []
        self.hompage.append(hompage)
    
    def add_seeAlso(self,seeAlso):
        if unused(self.seeAlso):
            self.seeAlso = []
        self.seeAlso.append(seeAlso)


class hompage(CoreAttributes):
    """https://iiif.io/api/presentation/3.0/#homepage
    """
    def __init__(self):
        super(hompage, self).__init__()
        self.language = None
        self.format = Suggested()
    
    def set_language(self,language):
        if unused(self.language):
            self.language = []
        self.language.append(language)

    def set_format(self,format):
        self.format = format
    
    def set_type(self,mtype):
        self.type = mtype
        
class logo(CoreAttributes,plus.HeightWidthDuration):
    """
    A small image resource that represents the Agent resource it is associated with.
    The logo must be clearly rendered when the resource is displayed or used, 
    without cropping, rotating or otherwise distorting the image. It is recommended that
    a IIIF Image API service be available for this image for other manipulations 
    such as resizing.

    When more than one logo is present, the client should pick only one of them, based on the information in the logo properties. For example, the client could select a logo of appropriate aspect ratio based on the height and width properties of the available logos. The client may decide on the logo by inspecting properties defined as extensions.
    
    "logo": [
    {
      "id": "https://example.org/img/logo.jpg",
      "type": "Image",
      "format": "image/jpeg",
      "height": 100,
      "width": 120
    }
    ]
    #TODO Duration should not be included
    """
    def __init__(self):
        super(logo, self).__init__()
        self.format = Suggested()
        self.service = Suggested()
    
    def set_format(self,format):
        self.format = format
    
    def set_type(self,mtype):
        self.type = mtype

    def set_label(self,label):
        ValueError("Label not permitted in logo.")
    
    def add_service(self,service):
        if unused(self.service):
            self.service = []
        self.service.append(service)

class rendering(CoreAttributes):
    """
    https://iiif.io/api/presentation/3.0/#rendering
    A resource that is an alternative, non-IIIF representation
    of the resource that has the rendering property.
    Such representations typically cannot be painted onto a 
    single Canvas, as they either include too many views, 
    have incompatible dimensions, or are compound resources 
    requiring additional rendering functionality. 
    The rendering resource must be able to be displayed
    directly to a human user, although the presentation may
    be outside of the IIIF client. The resource must not 
    have a splash page or other interstitial resource that 
    mediates access to it. If access control is required, 
    then the IIIF Authentication API is recommended. 
    Examples include a rendering of a book as a PDF or EPUB,
    a slide deck with images of a building, or a 3D model 
    of a statue.

    "rendering": [
    {
      "id": "https://example.org/1.pdf",
      "type": "Text",
      "label": { "en": [ "PDF Rendering of Book" ] },
      "format": "application/pdf"
    }
    ]
    """
    def __init__(self):
        super(rendering, self).__init__()
        self.format = Suggested()
    
    def set_format(self,format):
        self.format = format
    
    def set_type(self,type):
        self.type = type 

class services(CoreAttributes):
    """
    A list of one or more service definitions on the 
    top-most resource of the document, that are typically 
    shared by more than one subsequent resource. 
    This allows for these shared services to be collected 
    together in a single place, rather than either having 
    their information duplicated potentially many times 
    throughout the document, or requiring a consuming client
    to traverse the entire document structure to find the
    information. The resource that the service applies to
    must still have the service property, as described
    above, where the service resources have at least the id
    and type or @id and @type properties. This allows the 
    client to know that the service applies to that resource.
    Usage of the services property is at the discretion of 
    the publishing system.
    """
    def __init__(self):
        super(services, self).__init__()
        self.profile = Suggested()
        self.service = Required()
    
    def set_profile(self,profile):
        self.profile = profile

    def add_service(self,service):
        if unused(self.service):
            self.service = []
        self.service.append(service)


class start(CommonAttributes):

    def __init__(self):
        super(start, self).__init__()
        self.profile = Suggested()
        self.source = None
        self.selector = None
    
    def set_type(self,mtype):
        if mtype is not "Canvas":
            self.source = Required("If you are not pointing to a Canvas please specify a source.")
            self.selector = Required("If you are not pointing to a Canvas please specify a selector")
        self.type = mtype
    
    def set_source(self,source):
        self.set_source = source
    
    def set_selector(self,selector):
        self.selector = selector

 #json.dumps(g, default=lambda x:x.__dict__)
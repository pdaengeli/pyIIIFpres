# implementation of Metadata on any Resource https://iiif.io/api/cookbook/recipe/0029-metadata-anywhere/
from IIIFpres import iiifpapi3
iiifpapi3.BASE_URL = r"https://iiif.io/api/cookbook/recipe/0029-metadata-anywhere/"
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest.json")
manifest.add_label("en","John Dee performing an experiment before Queen Elizabeth I.")
manifest.add_metadata(
    label="Creator", value="Glindoni, Henry Gillard, 1852-1913", language_l="en", language_v="en")
manifest.add_metadata(label="Date", value="1800-1899", language_l="en", language_v="en")
manifest.add_metadata(
    label="Physical Description",
    value="1 painting : oil on canvas ; canvas 152 x 244.4 cm",
    language_l="en",language_v="en")
manifest.add_metadata(label="Reference",value="Wellcome Library no. 47369i",language_l="en",language_v="en")
reqst = manifest.add_requiredStatement()
reqst.add_label(language="en",label="Attribution")
reqst.add_value(language="en",value="Wellcome Collection. Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)")
canvas = manifest.add_canvas_to_items()
canvas.set_id(extendbase_url="canvas/p1")
canvas.add_label("en","Painting under natural light")
canvas.set_height(1271)
canvas.set_width(2000)
cnvmetdata = canvas.add_metadata()
cnvmetdata.add_label(language="en",label="Description")
cnvmetdata.add_value(language="en",value="The scene is the house at Mortlake of Dr John Dee (1527-1608). At the court of Queen Elizabeth I, Dee was revered for the range of his scientific knowledge, which embraced the fields of mathematics, navigation, geography, alchemy/chemistry, medicine and optics. In the painting he is showing the effect of combining two elements, either to cause combustion or to extinguish it. Behind him is his assistant Edward Kelly, wearing a long skullcap to conceal the fact that his ears had been cropped as a punishment for forgery.")
annopage = canvas.add_annotationpage_to_items()
annopage.set_id(extendbase_url="page/p1/1")
annotation = annopage.add_annotation_to_items(target=canvas.id) 
annotation.set_motivation("painting")
annotation.set_id(extendbase_url="annotation/p0001-image")
annotation.body.set_height(1271)
annotation.body.set_width(2000)
annotation.body.set_id(r"https://iiif.io/api/image/3.0/example/reference/421e65be2ce95439b3ad6ef1f2ab87a9-dee-natural/full/max/0/default.jpg")
annotation.body.set_format("image/jpg")
annotation.body.set_type("Image")
srv = annotation.body.add_service()
srv.set_id("https://iiif.io/api/image/3.0/example/reference/421e65be2ce95439b3ad6ef1f2ab87a9-dee-natural")
srv.set_profile("level1")
srv.set_type("ImageService3")

# X-ray
canvas = manifest.add_canvas_to_items()
canvas.set_id(extendbase_url=["canvas","p2"])
canvas.add_label("en","X-ray view of painting")
canvas.set_height(1271)
canvas.set_width(2000)
cnvmetdata = canvas.add_metadata()
cnvmetdata.add_label(language="en",label="Description")
cnvmetdata.add_value(language="en",value="The painting originally showed Dee standing in a circle of skulls on the floor, stretching from the floor area in front of the Queen (on the left) to the floor near Edward Kelly (on the right). The skulls were at an early stage painted over, but have since become visible. Another pentimento is visible in the tapestry on the right: shelves containing monstrous animals are visible behind it. The pentimenti were clarified when the painting was X-rayed in 2015.")
manifest.json_save("0007-string-formats-manifest.json")
annopage = canvas.add_annotationpage_to_items()
annopage.set_id(extendbase_url=["page","p2","1"])
annotation = annopage.add_annotation_to_items(target=canvas.id) 
annotation.set_motivation("painting")
annotation.set_id(extendbase_url=["annotation","p0002-image"])
annotation.body.set_height(1271)
annotation.body.set_width(2000)
annotation.body.set_id(r"https://iiif.io/api/image/3.0/example/reference/421e65be2ce95439b3ad6ef1f2ab87a9-dee-xray/full/max/0/default.jpg")
annotation.body.set_format("image/jpg")
annotation.body.set_type("Image")
srv = annotation.body.add_service()
srv.set_id("https://iiif.io/api/image/3.0/example/reference/421e65be2ce95439b3ad6ef1f2ab87a9-dee-xray")
srv.set_profile("level1")
srv.set_type("ImageService3")
manifest.json_save("0029-metadata-anywhere-manifest.json")


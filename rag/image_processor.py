import fitz
import os


def extract_images(pdf_path, output_folder="uploads/images"):

    os.makedirs(output_folder, exist_ok=True)

    doc = fitz.open(pdf_path)

    images = []

    for page_number, page in enumerate(doc):

        image_list = page.get_images(full=True)

        for image_index, img in enumerate(image_list):

            xref = img[0]

            base_image = doc.extract_image(xref)

            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_name = f"page_{page_number+1}_image_{image_index+1}.{image_ext}"

            image_path = os.path.join(
                output_folder,
                image_name
            )

            with open(image_path, "wb") as f:
                f.write(image_bytes)


            images.append({
                "page": page_number + 1,
                "path": image_path
            })


    return images
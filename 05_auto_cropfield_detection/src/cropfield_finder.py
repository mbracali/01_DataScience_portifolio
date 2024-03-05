"""This module is responsible to use SAM methods and draw polygons in crop
fields"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator

from .transformers import ImgTransformers


class FindWithSam:  # pylint: disable=R0902
    """This class is destined to concentrate all methods of the
    cropfield auto finder. Every method should be commented in
    with the sphynx format so it can be easily documented and
    readed by anyone."""

    def __init__(self, model_path="model/sam_vit_h_4b8939.pth",
                 model_type="vit_h", use_gpu=False):
        """Constructor method who also loads the SAM model, witch
        needs to be downloaded outside the lib. You NEED to enforce the
        model type as well, models can be downloaded:
        2.5gb
        https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth
        1.2gb
        https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth
        ~400mb
        -https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth

        :param model_path: Path to SAM model, default:"model/vit_h_4b8939.pth"
        :type model_path: str, optional
        :param model_type: Inform wich model should be used, only 3
            values are possible:
            "vit_h": When using the HUGE sam model
            "vit_l": When using the LARGE sam model
            "vit_b": When using the BIG sam model
            defaults to "vit_h"
        :type model_type: str, optional
        :param use_gpu: If you have a NVIDIA GPU with more than 6gb of
            memory, is possible to se this atribute to True and use
            CUDA CORES to process the model, defaults to False
        :type use_gpu: bool, optional
        """

        self.sam_checkpoint = model_path
        self.model_type = model_type
        self.default_image = None
        self.mask_generator = None
        self.masks = None
        self.it_obj = None

        if use_gpu:
            self.devices = "cuda"
        else:
            self.devices = "cpu"

        self.sam = sam_model_registry[self.model_type](
            checkpoint=self.sam_checkpoint
            )

        self.sam.to(self.devices)

    def enhance_img(self, method, show_image=False, save_after=False):
        """This method offer a different array of enhancers.
        These enhancers are used to make the classification easy.
        If a imagem is not beeing classified correctly, try to use one of the
        avaliable enhancers before the classification.

        :param method: Specifyes what enhancer you want to use
        :type method: string
        :param show_image: If True, show the image after enhancing,
            defaults to False
        :type show_image: bool, optional
        :param save_after: If True, replaces the default image,
            defaults to False
        :type save_after: bool, optional
        """

        self.it_obj = ImgTransformers()

        self.it_obj.set_img(self.default_image)

        if isinstance(method) == list:
            transformed_img = self.it_obj.transform_list(method)

        if isinstance(method) == str:
            transformed_img = self.it_obj.transform(method)

        if show_image:
            plt.figure(figsize=(10, 10))
            plt.imshow(transformed_img)
            plt.axis("off")
            plt.show()

        if save_after:
            self.default_image = transformed_img

    def set_image(self, path_to_image, show_image=False):
        """This method set the default image to be used"

        :param path_to_image: Should have the image path
        :type path_to_image: string
        :param show_image: If True, show the image after seting,
            defaults to False
        :type show_image: bool, optional
        """

        # Set de default image and readit in the correct color code
        self.default_image = cv2.imread(path_to_image)
        self.default_image = cv2.cvtColor(self.default_image,
                                          cv2.COLOR_BGR2RGB)

        # If flag changed to True shows the image to the user
        if show_image:
            plt.figure(figsize=(10, 10))
            plt.imshow(self.default_image)
            plt.axis("off")
            plt.show()

    def transform(self, show_image=False, save_after=False,
                  path="./SAM_transformed.png"):
        """Apply SAM to the default image
        (You need's to set up a default image first)

        :param show_image: If True, show the image after the classifier,
            defaults to False
        :type show_image: bool, optional
        :param save_after: If True, replace the defalt image,
            defaults to False
        :type save_after: bool, optional
        :param path: Path to save, defaults to "./SAM_transformed.png"
        :type path: str, optionalß
        """

        self.sam.to(device=self.devices)
        self.mask_generator = SamAutomaticMaskGenerator(self.sam)
        self.masks = self.mask_generator.generate(self.default_image)

        # Process the image
        plt.figure(figsize=(10, 10))
        plt.imshow(self.default_image)
        self.show_anns(self.masks)
        plt.axis("off")
        if show_image:
            plt.show()
        if save_after:
            plt.savefig(path)

    def set_transform(self, path_to_image, show_image=False,
                      save_after=False, path="./SAM_transformed.png"):
        """This method is just a wrapper of the set and transform methods.
        All possible atributes of the set and transform methods are avaliable
        here.

        :param path_to_image: Should have the image path
        :type path_to_image: string
        :param show_image: If True, show the image after the classifier,
            defaults to False
        :type show_image: bool, optional
        :param save_after: If True, replace the defalt image,
            defaults to False
        :type save_after: bool, optional
        :param path: Path to save, defaults to "./SAM_transformed.png"
        :type path: str, optional
        """

        # Seting the image
        self.set_image(path_to_image=path_to_image,
                       show_image=show_image)

        # Creating masks
        self.transform(show_image=show_image, save_after=save_after,
                       path=path)

    def serialize_masks(self, path="masks.txt"):
        """Calling this method make the masks of each classified object,
        to be serialized into the system.
        (Objects will be saved into JSON format)

        :param path: Where into the system the masks should be saved
        :type path: string
        """
        np.savetxt(path, self.masks, fmt='%s')

    @staticmethod
    def show_anns(anns):
        """This static function is responsible to draw
        the polygons on the map

        :param anns: Expects a array of numbers
        :type anns: numpy array
        """

        if len(anns) == 0:
            return

        # Sort the polygons
        sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)

        axis = plt.gca()
        axis.set_autoscale_on(False)
        # polygons = []
        # color = []

        # For each polygon draw the polygon into the image
        for ann in sorted_anns:

            # We just pick any name here
            metric = ann['segmentation']

            # Just create a simple image
            img = np.ones((metric.shape[0], metric.shape[1], 3))

            # Pick a randon color for each polygon
            color_mask = np.random.random((1, 3)).tolist()[0]

            for i in range(3):

                # Draw the polygon
                img[:, :, i] = color_mask[i]

            # Show the image
            axis.imshow(np.dstack((img, metric*0.35)))

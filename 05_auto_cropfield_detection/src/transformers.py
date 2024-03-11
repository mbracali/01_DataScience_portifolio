"""
[PT-BR]
Essa classe tem como o unico objetivo a aplicacao de transformacoes
classicas da literatura em imagens de qualquer natureza. Ainda que
pensada para ser utilizada no projeto de talhonamento automatizado
Nutrien, a sua utilizacao pode ser extendida para qualquer outra
implementacao.
Caso seja sua primeira vez lidando com esse tipo de assunto a leitura
do seguinte e recomendada:
https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html

[EN-EN]
This class have only one objective, witch is to apply classic image
transformation in any image. Developed to be used in pair with the
automatic cropfiled finder but not limited to, the utilization of this
class is extensible to any scenario where it can bem applyed.
If this is your first time using image transformations, we suggest
reading the following:
https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


class ImgTransformers:
    """This class has the objective to provide image transformers
    """

    def __init__(self):
        """Class constructor
        """

        self.img = None
        self.bkp_img = None

        self.transformers = {
            "simple_blur": self.simple_blur,
            "erode": self.erode,
            "dilate": self.dilate,
            "opening": self.opening,
            "closing": self.closing,
            "morph_gradient": self.morph_gradient,
            "top_hat": self.top_hat,
            "black_hat": self.black_hat,
            "erode_dilate": self.erode_dilate,
            "dilate_erode": self.dilate_erode,
        }

    def set_img(self, img, show_img=False):
        """Inspired by the scikit-learn way, this class provides a method to
        set a default image (fit on sklearn) and another one to transform the
        default image. This method requires a img imported in a open-cv
        compatible format.

        :param img: The image where we want to aplly the transformations
        :type img: Open-cv compatible img format (np-array works)
        :param img: Show the image after seting it
        :type img: bool
        :param show_img: Show image after seting it
        :type show_img: bool
        """

        self.img = img

        self.bkp_img = img

        # If flag changed to True shows the image to the user
        if show_img:
            plt.figure(figsize=(10, 10))
            plt.imshow(self.img)
            plt.axis("off")
            plt.show()

    def transform(self, how, show_img=False):
        """Responsible to force the transformation on the default setted img.

        :param how: The transform method should be explicited here
        :type how: string
        :param show_img: if True shows transformed image, defaults to False
        :type show_img: bool, optional
        :return: Returns transformed image, on fail returns False
        :rtype: open-cv compatible image type
        """

        # This block is responsible for understand what methods are possible
        # to be called. This implementation can be further improved raising
        # propper errors as it should.
        if how not in self.transformers:
            print("""You should select one of the possible methods to transform
                  your image. This method will return a False bool object.
                  The implemented transformers are:""")
            print(self.transformers.keys())

            return self.img

        # Perform the transformation itself
        self.img = self.transformers[how](self.img)

        # If flag changed to True shows the image to the user
        if show_img:
            plt.figure(figsize=(10, 10))
            plt.imshow(self.img)
            plt.axis("off")
            plt.show()

        return self.img

    def transform_list(self, transform_list: list, show_img=False):
        """Perform multiple transformations in a image. You should provide a
        list with all the implemented transformations in order.
        First element of the list will be the first transformation, last
        element will be the last transformation.
        Each transformation will overwrite the last one, be careful with your
        image, you may lost the original one.

        :param transform_list: The list with all transformations to perform
        :type transform_list: list
        :param show_img: If True, shows the transformation, defaults to False
        :type show_img: bool, optional
        :return: Returns the transformed image
        :rtype: Open-cv compatible image or image extension
        """

        # This block performs a check with the transform list variable
        if (len(transform_list) < 1) or isinstance(transform_list) != list:
            print("""
            You should provide a list with elements!
            The elements must be implemented functions, list of all
            implemented functions: """)
            print(self.transformers.keys())

        for transformation in transform_list:

            # For each element in the list, this loop runs a transformation
            # method on top of it.
            self.img = self.transform(transformation)

        # If flag changed to True shows the image to the user
        if show_img:
            plt.figure(figsize=(10, 10))
            plt.imshow(self.img)
            plt.axis("off")
            plt.show()

        return self.img

    def regenerate_img(self):
        """This method is responsible to restore the image to its default
        state.
        """

        self.img = self.bkp_img

    @staticmethod
    def simple_blur(img):
        """Apply the blur effect on a open-cv comptabile image

        :param img: The image to be transformed
        :type img: open-cv compatible image
        :return: The procesed image
        :rtype: open-cv compatible imagem
        """

        img = cv2.blur(img, (15, 15))

        return img

    @staticmethod
    def erode(img):
        """Apply the erode effect on a open-cv comptabile image

        :param img: The image to be transformed
        :type img: open-cv compatible image
        :return: The procesed image
        :rtype: open-cv compatible imagem
        """

        # Some effects needs to have a kernel to specify where the processing
        # effect should take place into the image, this lib uses a simple
        # kernel, if you need a more elaborated one is recommended to use.
        kernel = np.ones((3, 3), np.uint8)

        img = cv2.erode(img, kernel)

        return img

    @staticmethod
    def dilate(img):
        """Apply the dilate effect on a open-cv comptabile image

        :param img: The image to be transformed
        :type img: open-cv compatible image
        :return: The procesed image
        :rtype: open-cv compatible imagem
        """

        # Some effects needs to have a kernel to specify where the processing
        # effect should take place into the image, this lib uses a simple
        # kernel, if you need a more elaborated one is recommended to use.
        kernel = np.ones((5, 5), np.uint8)
        img = cv2.dilate(img, kernel)

        return img

    @staticmethod
    def opening(img):
        """Apply the opening effect on a open-cv comptabile image

        :param img: The image to be transformed
        :type img: open-cv compatible image
        :return: The procesed image
        :rtype: open-cv compatible imagem
        """

        # Some effects needs to have a kernel to specify where the processing
        # effect should take place into the image, this lib uses a simple
        # kernel, if you need a more elaborated one is recommended to use.
        kernel = np.ones((6, 6), np.uint8)

        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

        return img

    @staticmethod
    def closing(img):
        """Apply the closing effect on a open-cv comptabile image

        :param img: The image to be transformed
        :type img: open-cv compatible image
        :return: The procesed image
        :rtype: open-cv compatible imagem
        """

        # Some effects needs to have a kernel to specify where the processing
        # effect should take place into the image, this lib uses a simple
        # kernel, if you need a more elaborated one is recommended to use.
        kernel = np.ones((5, 5), np.uint8)

        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

        return img

    @staticmethod
    def morph_gradient(img):
        """Apply the morph-gradient effect on a open-cv comptabile image

        :param img: The image to be transformed
        :type img: open-cv compatible image
        :return: The procesed image
        :rtype: open-cv compatible imagem
        """

        # Some effects needs to have a kernel to specify where the processing
        # effect should take place into the image, this lib uses a simple
        # kernel, if you need a more elaborated one is recommended to use.
        kernel = np.ones((5, 5), np.uint8)

        img = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

        return img

    @staticmethod
    def top_hat(img):
        """Apply the top-hat effect on a open-cv comptabile image

        :param img: The image to be transformed
        :type img: open-cv compatible image
        :return: The procesed image
        :rtype: open-cv compatible imagem
        """

        # Some effects needs to have a kernel to specify where the processing
        # effect should take place into the image, this lib uses a simple
        # kernel, if you need a more elaborated one is recommended to use.
        kernel = np.ones((20, 20), np.uint8)

        img = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

        return img

    @staticmethod
    def black_hat(img):
        """Apply the black-hat effect on a open-cv comptabile image

        :param img: The image to be transformed
        :type img: open-cv compatible image
        :return: The procesed image
        :rtype: open-cv compatible imagem
        """

        # Some effects needs to have a kernel to specify where the processing
        # effect should take place into the image, this lib uses a simple
        # kernel, if you need a more elaborated one is recommended to use.
        kernel = np.ones((20, 20), np.uint8)

        img = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

        return img

    @staticmethod
    def erode_dilate(img):
        """Apply the erode + dilate effect on a open-cv comptabile image

        :param img: The image to be transformed
        :type img: open-cv compatible image
        :return: The procesed image
        :rtype: open-cv compatible imagem
        """

        # Some effects needs to have a kernel to specify where the processing
        # effect should take place into the image, this lib uses a simple
        # kernel, if you need a more elaborated one is recommended to use.
        kernel = np.ones((5, 5), np.uint8)

        img = cv2.erode(img, kernel)

        img = cv2.dilate(img, kernel)

        return img

    @staticmethod
    def dilate_erode(img):
        """Apply the dilate + erode effect on a open-cv comptabile image

        :param img: The image to be transformed
        :type img: open-cv compatible image
        :return: The procesed image
        :rtype: open-cv compatible imagem
        """

        # Some effects needs to have a kernel to specify where the processing
        # effect should take place into the image, this lib uses a simple
        # kernel, if you need a more elaborated one is recommended to use.
        kernel = np.ones((10, 10), np.uint8)

        img = cv2.dilate(img, kernel)

        img = cv2.erode(img, kernel)

        return img

# Copyright 2017, Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import unittest

import mock

from google.auth.credentials import Credentials
from google.cloud import vision


class DecoratorTests(unittest.TestCase):
    def test_noop_without_enums(self):
        class A(object):
            pass
        APrime = vision.decorators.add_single_feature_methods(A)

        # It should be the same class object.
        assert A is APrime

        # Nothing should have been added.
        assert not hasattr(A, 'face_detection')
        assert not hasattr(A, 'logo_detection')

    def test_with_enums(self):
        class A(object):
            enums = vision.enums

        # There should not be detection methods yet.
        assert not hasattr(A, 'face_detection')

        # Add the detection methods.
        APrime = vision.decorators.add_single_feature_methods(A)
        assert A is APrime

        # There should be detection methods now.
        assert hasattr(A, 'face_detection')
        assert callable(A.face_detection)


class SingleFeatureMethodTests(unittest.TestCase):
    @mock.patch.object(vision.ImageAnnotatorClient, 'annotate_image')
    def test_runs_generic_single_image(self, ai):
        ai.return_value = vision.types.AnnotateImageResponse()

        # Make a face detection request.
        client = vision.ImageAnnotatorClient(
            credentials=mock.Mock(spec=Credentials),
        )
        image = {'source': {'image_uri': 'gs://my-test-bucket/image.jpg'}}
        response = client.face_detection(image)

        # Assert that the single-image method was called as expected.
        ai.assert_called_once_with({
            'features': [{'type': vision.enums.Feature.Type.FACE_DETECTION}],
            'image': image,
        }, options=None)

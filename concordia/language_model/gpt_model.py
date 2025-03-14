# Copyright 2023 DeepMind Technologies Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Language Model that uses OpenAI's GPT models."""

import os
import openai
from concordia.language_model import language_model
from concordia.utils import measurements as measurements_lib
from concordia.language_model.base_gpt_model import BaseGPTModel


class GptLanguageModel(BaseGPTModel):
  """Language Model that uses OpenAI GPT models."""

  def __init__(
      self,
      model_name: str,
      *,
      api_key: str | None = None,
      measurements: measurements_lib.Measurements | None = None,
      channel: str = language_model.DEFAULT_STATS_CHANNEL,
      use_azure: bool = False,
      azure_endpoint: str | None = None,
  ):
    """Initializes the instance.

    Args:
      model_name: The language model to use. For more details, see
        https://platform.openai.com/docs/guides/text-generation/which-model-should-i-use.
      api_key: The API key to use when accessing the OpenAI API. If None, will
        use the OPENAI_API_KEY environment variable.
      measurements: The measurements object to log usage statistics to.
      channel: The channel to write the statistics to.
      use_azure: Whether to use Azure OpenAI Service.
      azure_endpoint: The endpoint for Azure OpenAI Service.
    """
    if api_key is None:
      api_key = os.environ['OPENAI_API_KEY']
    self._api_key = api_key

    if use_azure:
      client = openai.AzureOpenAI(
          api_key=self._api_key,
          azure_endpoint=azure_endpoint,
      )
    else:
      client = openai.OpenAI(api_key=self._api_key)

    super().__init__(model_name=model_name,
                     client=client,
                     measurements=measurements,
                     channel=channel)

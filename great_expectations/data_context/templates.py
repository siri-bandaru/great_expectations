# -*- coding: utf-8 -*-
import os
import uuid
from typing import Union

from jinja2 import DictLoader, Environment

INSTANCE_ID: str = f"{str(uuid.uuid4())}{os.linesep}"


CONFIG_VERSION_TEMPLATE: str = """
# config_version refers to the syntactic version of this config file, and is used in maintaining backwards compatibility
# It is auto-generated and usually does not need to be changed.
config_version: 2
"""

# noinspection SpellCheckingInspection
ANONYMIZED_USAGE_STATISTICS_TEMPLATE: str = """
anonymous_usage_statistics:
  enabled: {{ allow_anonymous_usage_statistics }}
"""

DATA_CONTEXT_UNIQUE_ID_PROJECT_TEMPLATE: str = """
{% include 'config_version_template.j2' %}
{% include 'anonymized_usage_statistics_template.j2' %}
"""

PROJECT_HELP_COMMENT_TEMPLATE: str = """
# Welcome to Great Expectations! Always know what to expect from your data.
#
# Here you can define datasources, batch kwargs generators, integrations and
# more. This file is intended to be committed to your repo. For help with
# configuration please:
#   - Read our docs: https://docs.greatexpectations.io/en/latest/how_to_guides/spare_parts/data_context_reference.html#configuration
#   - Join our slack channel: http://greatexpectations.io/slack

{% include 'config_version_template.j2' %}

# Datasources tell Great Expectations where your data lives and how to get it.
# You can use the CLI command `great_expectations datasource new` to help you
# add a new datasource. Read more at https://docs.greatexpectations.io/en/latest/reference/core_concepts/datasource_reference.html
datasources: {}
"""

CONFIG_VARIABLES_INTRO_TEMPLATE: str = """
# This config file supports variable substitution which enables: 1) keeping
# secrets out of source control & 2) environment-based configuration changes
# such as staging vs prod.
#
# When GE encounters substitution syntax (like `my_key: ${my_value}` or
# `my_key: $my_value`) in the great_expectations.yml file, it will attempt
# to replace the value of `my_key` with the value from an environment
# variable `my_value` or a corresponding key read from this config file,
# which is defined through the `config_variables_file_path`.
# Environment variables take precedence over variables defined here.
#
# Substitution values defined here can be a simple (non-nested) value,
# nested value such as a dictionary, or an environment variable (i.e. ${ENV_VAR})
#
#
# https://docs.greatexpectations.io/en/latest/how_to_guides/configuring_data_contexts/how_to_use_a_yaml_file_or_environment_variables_to_populate_credentials.html

"""

CONFIG_VARIABLES_TEMPLATE: str = """
{% include 'config_variables_intro_template.j2' %}
instance_id: {{ instance_id }}
"""

PROJECT_OPTIONAL_CONFIG_COMMENT_TEMPLATE: str = """
{% include 'config_variables_intro_template.j2' %}
config_variables_file_path: uncommitted/config_variables.yml

# The plugins_directory will be added to your python path for custom modules
# used to override and extend Great Expectations.
plugins_directory: plugins/

# Validation Operators are customizable workflows that bundle the validation of
# one or more expectation suites and subsequent actions. The example below
# stores validations and send a slack notification. To read more about
# customizing and extending these, read: https://docs.greatexpectations.io/en/latest/reference/core_concepts/validation_operators_and_actions.html
validation_operators:
  action_list_operator:
    # To learn how to configure sending Slack notifications during evaluation
    # (and other customizations), read: https://docs.greatexpectations.io/en/latest/autoapi/great_expectations/validation_operators/index.html#great_expectations.validation_operators.ActionListValidationOperator
    class_name: ActionListValidationOperator
    action_list:
      - name: store_validation_result
        action:
          class_name: StoreValidationResultAction
      - name: store_evaluation_params
        action:
          class_name: StoreEvaluationParametersAction
      - name: update_data_docs
        action:
          class_name: UpdateDataDocsAction
      # - name: send_slack_notification_on_validation_result
      #   action:
      #     class_name: SlackNotificationAction
      #     # put the actual webhook URL in the uncommitted/config_variables.yml file
      #     slack_webhook: ${validation_notification_slack_webhook}
      #     notify_on: all # possible values: "all", "failure", "success"
      #     renderer:
      #       module_name: great_expectations.render.renderer.slack_renderer
      #       class_name: SlackRenderer

stores:
# Stores are configurable places to store things like Expectations, Validations
# Data Docs, and more. These are for advanced users only - most users can simply
# leave this section alone.
#
# Three stores are required: expectations, validations, and
# evaluation_parameters, and must exist with a valid store entry. Additional
# stores can be configured for uses such as data_docs, validation_operators, etc.
  expectations_store:
    class_name: ExpectationsStore
    store_backend:
      class_name: TupleFilesystemStoreBackend
      base_directory: expectations/

  validations_store:
    class_name: ValidationsStore
    store_backend:
      class_name: TupleFilesystemStoreBackend
      base_directory: uncommitted/validations/

  evaluation_parameter_store:
    # Evaluation Parameters enable dynamic expectations. Read more here:
    # https://docs.greatexpectations.io/en/latest/reference/core_concepts/evaluation_parameters.html
    class_name: EvaluationParameterStore

expectations_store_name: expectations_store
validations_store_name: validations_store
evaluation_parameter_store_name: evaluation_parameter_store

data_docs_sites:
  # Data Docs make it simple to visualize data quality in your project. These
  # include Expectations, Validations & Profiles. The are built for all
  # Datasources from JSON artifacts in the local repo including validations &
  # profiles from the uncommitted directory. Read more at https://docs.greatexpectations.io/en/latest/reference/core_concepts/data_docs.html
  local_site:
    class_name: SiteBuilder
    # set to false to hide how-to buttons in Data Docs
    show_how_to_buttons: true
    store_backend:
        class_name: TupleFilesystemStoreBackend
        base_directory: uncommitted/data_docs/local_site/
    site_index_builder:
        class_name: DefaultSiteIndexBuilder
"""

# noinspection SpellCheckingInspection
PROJECT_TEMPLATE_WITH_USAGE_STATISTICS_TEMPLATE: str = """
{% include 'project_help_comment_template.j2' %}
{% include 'project_optional_config_comment_template.j2' %}
{% include 'anonymized_usage_statistics_template.j2' %}
"""

# noinspection SpellCheckingInspection
J2_ENV: Environment = Environment(
    loader=DictLoader(
        {
            "config_version_template.j2": CONFIG_VERSION_TEMPLATE,
            "anonymized_usage_statistics_template.j2": ANONYMIZED_USAGE_STATISTICS_TEMPLATE,
            "data_context_unique_id_project_template.j2": DATA_CONTEXT_UNIQUE_ID_PROJECT_TEMPLATE,
            "project_help_comment_template.j2": PROJECT_HELP_COMMENT_TEMPLATE,
            "config_variables_intro_template.j2": CONFIG_VARIABLES_INTRO_TEMPLATE,
            "config_variables_template.j2": CONFIG_VARIABLES_TEMPLATE,
            "project_optional_config_comment_template.j2": PROJECT_OPTIONAL_CONFIG_COMMENT_TEMPLATE,
            "project_template_with_usage_statistics_template.j2": PROJECT_TEMPLATE_WITH_USAGE_STATISTICS_TEMPLATE,
        }
    )
)


def get_project_config_yaml(j2_template_name: str, **kwargs) -> Union[str, None]:
    if j2_template_name is None or len(j2_template_name) < 4:
        return None
    return J2_ENV.get_template(j2_template_name).render(kwargs)

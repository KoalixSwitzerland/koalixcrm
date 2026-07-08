from koalixcrm.reporting.tests.factories.agreement_factory import (
    StandardAgreementToTaskFactory,
    StandardHumanResourceAgreementToTaskFactory,
)
from koalixcrm.reporting.tests.factories.agreement_status_factory import (
    AgreedAgreementStatusFactory,
    PlannedAgreementStatusFactory,
    StartedAgreementStatusFactory,
)
from koalixcrm.reporting.tests.factories.agreement_type_factory import (
    StandardAgreementTypeFactory,
)
from koalixcrm.reporting.tests.factories.estimation_factory import (
    StandardEstimationToTaskFactory,
    StandardHumanResourceEstimationToTaskFactory,
)
from koalixcrm.reporting.tests.factories.estimation_status_factory import (
    ObsoleteEstimationStatusFactory,
    PlannedEstimationStatusFactory,
    StartedEstimationStatusFactory,
)
from koalixcrm.reporting.tests.factories.generic_project_link_factory import (
    LinkToTaskGenericTaskLinkFactory,
)
from koalixcrm.reporting.tests.factories.generic_task_link_factory import (
    LinkToProjectGenericTaskLinkFactory,
)
from koalixcrm.reporting.tests.factories.human_resource_factory import (
    StandardHumanResourceFactory,
)
from koalixcrm.reporting.tests.factories.project_factory import StandardProjectFactory
from koalixcrm.reporting.tests.factories.project_link_type_factory import (
    RelatedToProjectLinkTypeFactory,
    RequiresProjectLinkTypeFactory,
)
from koalixcrm.reporting.tests.factories.project_status_factory import (
    DoneProjectStatusFactory,
    StartedProjectStatusFactory,
)
from koalixcrm.reporting.tests.factories.reporting_period_factory import (
    StandardReportingPeriodFactory,
)
from koalixcrm.reporting.tests.factories.reporting_period_status_factory import (
    DoneReportingPeriodStatusFactory,
    InPreparationReportingPeriodStatusFactory,
    ReportingReportingPeriodStatusFactory,
)
from koalixcrm.reporting.tests.factories.resource_factory import StandardResourceFactory
from koalixcrm.reporting.tests.factories.resource_manager_factory import (
    StandardResourceManagerFactory,
)
from koalixcrm.reporting.tests.factories.resource_price_factory import (
    HighResourcePriceFactory,
    StandardResourcePriceFactory,
)
from koalixcrm.reporting.tests.factories.resource_type_factory import StandardResourceTypeFactory
from koalixcrm.reporting.tests.factories.task_factory import StandardTaskFactory
from koalixcrm.reporting.tests.factories.task_link_type_factory import (
    RelatedToTaskLinkTypeFactory,
    RequiresLinkTypeFactory,
)
from koalixcrm.reporting.tests.factories.task_status_factory import (
    DoneTaskStatusFactory,
    PlannedTaskStatusFactory,
    StartedTaskStatusFactory,
)
from koalixcrm.reporting.tests.factories.work_factory import StandardWorkFactory

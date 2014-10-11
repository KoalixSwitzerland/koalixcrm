from django_states.machine import StateMachine, StateDefinition, StateTransition
from django.utils.translation import ugettext as _


class PurchaseStateMachine(StateMachine):
    log_transitions = True

    # possible states
    class initiated(StateDefinition):
        description = _('Purchase initiated')
        initial = True

    class paid(StateDefinition):
        description = _('Purchase paid')

    def handler(self, instance):
        pass

    class shipped(StateDefinition):
        description = _('Purchase shipped')

    # state transitions
    class mark_paid(StateTransition):
        from_state = 'initiated'
        to_state = 'paid'
        description = 'Mark this purchase as paid'

    class ship(StateTransition):
        from_state = 'paid'
        to_state = 'shipped'
        description = 'Ship purchase'

    def handler(transition, instance, user):
        pass

    def has_permission(transition, instance, user):
        return true_when_user_can_make_this_transition()
from django import template

register = template.Library()

@register.simple_tag
def user_bet(event, user):
    try:
        return event.bet_set.get(user=user).odd.name
    except:
        pass

@register.simple_tag
def bet_reward(event, user):
    try:
        if event.bet_set.get(user=user).odd.winner:
            return event.bet_set.get(user=user).odd.prize
    except:
        pass
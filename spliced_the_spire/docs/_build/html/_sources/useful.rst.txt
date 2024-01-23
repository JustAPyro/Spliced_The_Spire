Useful API's
************
The spliced the spire codebase has many abstractions that attempt
to simplify the creation of middle level code- The implementation of cards,
enemies, effects and relics. This page documents the methods most useful
to middle level development, organized by caller object.

Actor
=====

.. autoclass:: new.actors.AbstractActor

The actor abstraction represents the player, AI, or machine learning algorithm.
It manages traits owned by the player in slay the spire such as card decks,
drawing and discarding, effects, and so on. The following are useful methods the
AbstractActor provides to help give you information on these traits.

Card Information API
^^^^^^^^^^^^^^^^
|
.. autofunction:: new.actors.AbstractActor.get_draw
|
.. autofunction:: new.actors.AbstractActor.get_hand
|
.. autofunction:: new.actors.AbstractActor.draw_card
|
.. autofunction:: new.actors.AbstractActor.get_discard
|
.. autofunction:: new.actors.AbstractActor.discard_card
|
.. autofunction:: new.actors.AbstractActor.discard_hand
|
.. autofunction:: new.actors.AbstractActor.exhaust_card
|
Enemy
=====

Effects (Actor and Enemy)
=========================

.. autoclass:: new.effects.EffectMixin

The Effect Mixin is inherited by both Actors and Enemies. This
mixin provides abstractions related to effects to both of these children.
Power abilities are also represented by effects.

Actor/Enemy Effect API
^^^^^^^^^^^^^^^^^^^^^^

|
.. autofunction:: new.effects.EffectMixin.increase_effect
|
.. autofunction:: new.effects.EffectMixin.decrease_effect
|
.. autofunction:: new.effects.EffectMixin.set_effect
|
.. autofunction:: new.effects.EffectMixin.has_effect
|
.. autofunction:: new.effects.EffectMixin.stacks_of_effect





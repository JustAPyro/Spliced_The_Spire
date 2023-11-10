Contributing Cards
******************

You can contribute to the card implementation by designing cards that inherit from the AbstractCard class:

|
.. autoclass:: new.cards.AbstractCard
|

To use this abstraction, you are **required** to override two methods:

.. autofunction:: new.cards.AbstractCard.use
|
.. autofunction:: new.cards.AbstractCard.upgrade_logic
|

Additionally, you may **optionally** override the following methods to change the behavior of the card

.. autofunction:: new.cards.AbstractCard.is_playable



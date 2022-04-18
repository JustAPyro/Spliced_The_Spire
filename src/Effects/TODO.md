# Effects TODO:
This file contains information on all the Effects (buffs and debuffs) that need to be implemented in order to run Slay the Spire. 
It also contains tips and hints at implementations, and some comments by contributors.

## What information is provided?
  - Stack Type: Provides information on what the number of stacks does (See "What does Stack Type Mean?" below for more info)
  - Trigger: What makes the buff trigger, and (if applicable) the AbstractEffect method that I (Luke) think you should consider overriding to implement it.
  - Wiki: The wiki short description of the buff, note that these may be abbrivated or incomplete, refer to actual wiki for info.
  - Luke: My additional thoughts/comments about the effect- Additional contributors are welcome to add their own comments/replies under their name as well.


## What does Stack Type mean?
- Counter: Stacks determine how many times the effect happens- more stacks means it will happen more times.
- Intensity: Stacks determine the power- more stacks means the buff will be more effective
- Duration: Stacks determine how many turns the effect will last- More stacks means you'll have it more turns
- NO: Pretty straightforward- This effect doesn't stack- re-applying it provides no benefit

Note: Currently stacks are representing in the code using AbstractEffect.quantity or self.quantity- in many cases this variable is what X means.

## How to implement an effect:
Effects are built in a sandbox like way- You simply have to start by importing:  ```from src.Effects.AbstractEffect import AbstractEffect```
and then creating a class with the name of the effect you're creating that inherits from ```AbstractEffect```.
Start by defining an ```__init__()``` method that passes values into ```AbstractEffect.__init__(params)``` and once that's done you simply have to 
override any method based on when the effect triggers. Note that this is all you have to do- the methods themselves will be called automatically
by the subclass at the appropriate time. 

### Step by Step
If that seems confusing, simply follow these steps in order and you'll create a working Effect
1. Create a new class named ```EffectYouWantToImplement.py``` in the ```src.Effects``` folder.
2. Start by adding the import statement ```from src.Effects.AbstractEffect import AbstractEffect``` to the top of the new file.
3. Create a new class in the file that inherits from Abstract effect by using the following header signature: <br>```class EffectYouWantToImplement(AbstractEffect):```
4. Create an ```__init__()``` method in the new class. Generally this should take a target and a starting stack number. It will usually look something like this:
```def __init__(self, target, quantity=0):```
5. *INSIDE* that constructor, add the following call to the super-class constructor and pass in the necessary parameters: 
```
AbstractEffect.__init__(self, target,
                        name="NameOfEffectYouWantToImplement",
                        effectType="Buff", # Or De-buff
                        decreaseOverTime=False # Determines if you loose a stack each turn
                        quantity = quantty)
```
6. Now simply override the method you want the effect to trigger on. For example, you may override onTurnStart() if you want it to trigger at the start of each turn,
or onDamageDealt() if you want it to trigger when damage is dealt. See the docs for the methods you can override in the AbstractEffect class here: (TODO: FILL)
7. The last thing you should do is make sure that your Effect is properly exported from the package. This is easier then it sounds, I promise!
All you have to do is open the ```src/Effects/__init__.py``` file and add the line: <br>
```from src.Effects.EffectYouWantToImplement import *```
8. You're done! Great job.

### Example Effect Implementation
Here's a sample implementation for the Strength effect:

```
from src.Effects.AbstractEffect import AbstractEffect


class Strength(AbstractEffect):
    def __init__(self, target, quantity=0):
        AbstractEffect.__init__(self, target
                                name="Strength",
                                effectType="Buff",
                                decreaseOverTime=False
                                quantity=quantity)

    def modifyDamageDealt(self, dmg):
        return dmg + self.quantity
```
Once the class is defined like that, you simply need to add one line to the __init__.py file **in the *effects* folder**:
<br>```from src.Effects.EffectYouImplemented import *```

### Final notes:
Once your new class is created and merged with the main branch, I'll update the following list manually. However, if you would like to check it yourself, you simply
have to open the src/Effects/TODO.md file, scroll down to the ```## All Effects``` section, and look for the Effect you created. Once you find it, simply put an X in 
between the braces beside the Effect name, so it goes from ``` - [ ] EffectName:``` to ``` - [X] EffectName:```. Once this gets pushed to the main github page that 
will automatically update the Effect with a Checkmark.


## All Effects:

- [ ] Artifact:
  - Stack Type: Counter
  - Trigger: When a debuff is received
  - Wiki: Negates X Debuffs
  
- [ ] Buffer:
  - Stack Type: Counter
  - Trigger: When you loose HP
  - Wiki: Prevent the next X times you would lose HP
  
- [ ] Mantra: 
  - Stack Type: Counter
  - Trigger: When you get to quantity 10
  - Wiki: When you gain 10 mantra, enter divinity
  - Luke: ... and when entrying divnity, return to 0 stacks

- [ ] Dexterity:
  - Stack Type: Intensity
  - Trigger: When you gain block from a card
  - Wiki: Increase Block gained from cards by X
  
- [ ] Draw Card:
  - Stack Type: Intensity
  - Trigger: On your next turn
  - Wiki: Draw X Additional Cards next Turn
  - Luke: Wiki lists this with general buffs- but shouldn't this be with player buffs? Monster's can't have this, right?
  
- [ ] Energized:
  - Stack Type: Intensity
  - Trigger: On your next turn
  - Wiki: Gain X Additional Energy Next Turn
  
- [ ] Focus:
  - Stack Type: Intensity
  - Trigger: On orb trigger?
  - Wiki: Increase the effectiveness of Orbs by X
  - Luke: This one seems a bit complex. Again, shouldn't this be a player specific buff?
  
- [ ] Metallicize:
  - Stack Type: Intensity
  - Trigger: At the end of this turn
  - Wiki: At the end of your/its turn, gain X Block
  
- [ ] Next Turn Block:
  - Stack Type: Intensity
  - Trigger: On your next turn
  - Wiki: Gain X Block next turn
  
- [ ] Plated Armor:
  - Stack Type: Intensity
  - Trigger: At the end of this turn ALSO when receiving damage
  - Wiki: At the end of your turn gain X Block, receiving unblocked attack damage reduces PA by 1
  
- [ ] Regen:
  - Stack Type: Intensity
  - Trigger: At the end of this turn
  - Wiki: At the end of it's turn, Heals X HP
  - Luke: Pretty sure this also looses 1 every turn?
  
- [X] Ritual:
  - Stack Type: Intensity
  - Trigger: At the end of this turn
  - Wiki: At the end of it's turn, gains X Strength
  
- [X] Strength:
  - Stack Type: Intensity
  - Trigger: When you deal attack damage
  - Wiki: Increases attack damage by X
  - Luke: Curious about edge cases here, wikipedia specifies "attack damage" are there types of damage not affected by strength?
  
- [ ] Thorns:
  - Stack Type: Intensity
  - Trigger: When attacked
  - Wiki: When attacked, deals X Damage back
  
- [ ] Vigor:
  - Stack Type: Intensity
  - Trigger when you deal attack damage
  - Wiki: Your next attack deals X additional Damage
  - Luke: Is there a difference between this and Strength?

- [ ] Intangible
  - Stack Type: Duration
  - Trigger: On damage taken / lost
  - Wiki: Reduce ALL damage taken and HP loss to 1 this turn. (Lasts X Turns)
  - Luke: Question here: Will this also reduce damage to block? Or does it consume all block then deal 1 damage?

- [ ] Barricade:
  - Stack Type: NO
  - Trigger: On start of turn
  - Wiki: Block is not removed at the start of the Turn
  - Luke: This one seems a bit complicated to implement
  



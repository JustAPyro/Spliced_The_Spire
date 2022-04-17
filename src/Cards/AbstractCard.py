# blueprint for all cards

from abc import ABC, abstractmethod


# abstract card class
class AbstractCard(ABC):

    def __init__(self, name, energy_cost):

        # Name of the card
        self.name = name

        # normal energy cost of card ("cost" int)
        self.energyCost = energy_cost

        # energy cost for this turn ("costForTurn" int)
        self.energyCostForTurn = int

        # ("price" int)
        self.storePrice = int
        # ("chargeCost" int)
        # ("isCostModified" bool)
        # ("isCostModifiedForTurn" bool)
        # ("retain" bool)
        # ("selfRetain" bool)
        # ("dontTriggerOnUseCard" bool)
        # ("rarity" AbstractCard.CardRarity)
        # ("color" AbstractCard.CardColor)
        # ("isInnate" bool)
        # ("isLocked" bool)
        # ("showEvokeValue" bool)
        # ("showEvokeOrbCount" int)

        # public ArrayList<String> keywords;
        # private static final int COMMON_CARD_PRICE = 50;
        # private static final int UNCOMMON_CARD_PRICE = 75;
        # private static final int RARE_CARD_PRICE = 150;
        # protected boolean isUsed;
        # public boolean upgraded; is the card upgraded
        # public int timesUpgraded; how many times the card is upgraded
        # public int misc; ???
        # public int energyOnUse;
        # public boolean ignoreEnergyOnUse;
        # public boolean isSeen;
        # public boolean upgradedCost;
        # public boolean upgradedDamage;
        # public boolean upgradedBlock;
        # public boolean upgradedMagicNumber;
        # public UUID uuid;
        # public boolean isSelected;
        # public boolean exhaust;
        # public boolean returnToHand;
        # public boolean shuffleBackIntoDrawPile;
        # public boolean isEthereal;
        # public ArrayList<AbstractCard.CardTags> tags;
        # public int[] multiDamage;
        # protected boolean isMultiDamage;
        # public int baseDamage;
        # public int baseBlock;
        # public int baseMagicNumber;
        # public int baseHeal;
        # public int baseDraw;
        # public int baseDiscard;
        # public int damage;
        # public int block;
        # public int magicNumber;
        # public int heal;
        # public int draw;
        # public int discard;
        # public boolean isDamageModified;
        # public boolean isBlockModified;
        # public boolean isMagicNumberModified;
        # protected DamageType damageType;
        # public DamageType damageTypeForTurn;
        # public AbstractCard.CardTarget target;
        # public boolean purgeOnUse;
        # public boolean exhaustOnUseOnce;
        # public boolean exhaustOnFire;
        # public boolean freeToPlayOnce;
        # public boolean isInAutoplay;
        """
        private static TextureAtlas orbAtlas;
        private static TextureAtlas cardAtlas;
        private static TextureAtlas oldCardAtlas;
        public static AtlasRegion orb_red;
        public static AtlasRegion orb_green;
        public static AtlasRegion orb_blue;
        public static AtlasRegion orb_purple;
        public static AtlasRegion orb_card;
        public static AtlasRegion orb_potion;
        public static AtlasRegion orb_relic;
        public static AtlasRegion orb_special;
        public AtlasRegion portrait;
        public AtlasRegion jokePortrait;
        private static final UIStrings uiStrings;
        public static final String[] TEXT;
        public static float typeWidthAttack;
        public static float typeWidthSkill;
        public static float typeWidthPower;
        public static float typeWidthCurse;
        public static float typeWidthStatus;
        public static float typeOffsetAttack;
        public static float typeOffsetSkill;
        public static float typeOffsetPower;
        public static float typeOffsetCurse;
        public static float typeOffsetStatus;
        public AbstractGameEffect flashVfx;
        public String assetUrl;
        public boolean fadingOut;
        public float transparency;
        public float targetTransparency;
        private Color goldColor;
        private Color renderColor;
        private Color textColor;
        private Color typeColor;
        public float targetAngle;
        private static final float NAME_OFFSET_Y = 175.0F;
        private static final float ENERGY_TEXT_OFFSET_X = -132.0F;
        private static final float ENERGY_TEXT_OFFSET_Y = 192.0F;
        private static final int W = 512;
        public float angle;
        private ArrayList<CardGlowBorder> glowList;
        private float glowTimer;
        public boolean isGlowing;
        public static final float SMALL_SCALE = 0.7F;
        public static final int RAW_W = 300;
        public static final int RAW_H = 420;
        public static final float IMG_WIDTH;
        public static final float IMG_HEIGHT;
        public static final float IMG_WIDTH_S;
        public static final float IMG_HEIGHT_S;
        private static final float SHADOW_OFFSET_X;
        private static final float SHADOW_OFFSET_Y;
        public float current_x;
        public float current_y;
        public float target_x;
        public float target_y;
        protected Texture portraitImg;
        private boolean useSmallTitleFont;
        public float drawScale;
        public float targetDrawScale;
        private static final int PORTRAIT_WIDTH = 250;
        private static final int PORTRAIT_HEIGHT = 190;
        private static final float PORTRAIT_OFFSET_Y = 72.0F;
        private static final float LINE_SPACING = 1.45F;
        public boolean isFlipped;
        private boolean darken;
        private float darkTimer;
        private static final float DARKEN_TIME = 0.3F;
        public Hitbox hb;
        private static final float HB_W;
        private static final float HB_H;
        public float hoverTimer;
        private boolean renderTip;
        private boolean hovered;
        private float hoverDuration;
        private static final float HOVER_TIP_TIME = 0.2F;
        private static final GlyphLayout gl;
        private static final StringBuilder sbuilder;
        private static final StringBuilder sbuilder2;
        public AbstractCard cardsToPreview;
        protected static final float CARD_TIP_PAD = 16.0F;
        public float newGlowTimer;
        public String originalName;
        """
        # public String name;
        # public String cardID;
        """
        public ArrayList<DescriptionLine> description;
        public String cantUseMessage;
        private static final float TYPE_OFFSET_Y = -1.0F;
        private static final float DESC_OFFSET_Y;
        private static final float DESC_OFFSET_Y2 = -6.0F;
        private static final float DESC_BOX_WIDTH;
        private static final float CN_DESC_BOX_WIDTH;
        private static final float TITLE_BOX_WIDTH;
        private static final float TITLE_BOX_WIDTH_NO_COST;
        private static final float CARD_ENERGY_IMG_WIDTH;
        private static final float MAGIC_NUM_W;
        private static final UIStrings cardRenderStrings;
        public static final String LOCKED_STRING;
        public static final String UNKNOWN_STRING;
        private Color bgColor;
        private Color backColor;
        private Color frameColor;
        private Color frameOutlineColor;
        private Color frameShadowColor;
        private Color imgFrameColor;
        private Color descBoxColor;
        private Color bannerColor;
        private Color tintColor;
        private static final Color ENERGY_COST_RESTRICTED_COLOR;
        private static final Color ENERGY_COST_MODIFIED_COLOR;
        private static final Color FRAME_SHADOW_COLOR;
        private static final Color IMG_FRAME_COLOR_COMMON;
        private static final Color IMG_FRAME_COLOR_UNCOMMON;
        private static final Color IMG_FRAME_COLOR_RARE;
        private static final Color HOVER_IMG_COLOR;
        private static final Color SELECTED_CARD_COLOR;
        private static final Color BANNER_COLOR_COMMON;
        private static final Color BANNER_COLOR_UNCOMMON;
        private static final Color BANNER_COLOR_RARE;
        private static final Color CURSE_BG_COLOR;
        private static final Color CURSE_TYPE_BACK_COLOR;
        private static final Color CURSE_FRAME_COLOR;
        private static final Color CURSE_DESC_BOX_COLOR;
        private static final Color COLORLESS_BG_COLOR;
        private static final Color COLORLESS_TYPE_BACK_COLOR;
        private static final Color COLORLESS_FRAME_COLOR;
        private static final Color COLORLESS_DESC_BOX_COLOR;
        private static final Color RED_BG_COLOR;
        private static final Color RED_TYPE_BACK_COLOR;
        private static final Color RED_FRAME_COLOR;
        private static final Color RED_RARE_OUTLINE_COLOR;
        private static final Color RED_DESC_BOX_COLOR;
        private static final Color GREEN_BG_COLOR;
        private static final Color GREEN_TYPE_BACK_COLOR;
        private static final Color GREEN_FRAME_COLOR;
        private static final Color GREEN_RARE_OUTLINE_COLOR;
        private static final Color GREEN_DESC_BOX_COLOR;
        private static final Color BLUE_BG_COLOR;
        private static final Color BLUE_TYPE_BACK_COLOR;
        private static final Color BLUE_FRAME_COLOR;
        private static final Color BLUE_RARE_OUTLINE_COLOR;
        private static final Color BLUE_DESC_BOX_COLOR;
        protected static final Color BLUE_BORDER_GLOW_COLOR;
        protected static final Color GREEN_BORDER_GLOW_COLOR;
        protected static final Color GOLD_BORDER_GLOW_COLOR;
        """
        # public boolean inBottleFlame;
        # public boolean inBottleLightning;
        # public boolean inBottleTornado;
        # public Color glowColor;



    @abstractmethod
    def useCard(self, target):
        pass
    
    # Override the str() method so printing it returns the name
    def __str__(self):
        return self.name
        
    # Override the repr() method so arrays print neatly
    def __repr__(self):
        return self.name


"""
class strike(Card, ABC):

    def __init__(self):

        super().__init__()
        self.cardCost = 1

    def useCard(self):
        print("hit!")


myOnlyCard = strike()

print(myOnlyCard.cardCost)
"""

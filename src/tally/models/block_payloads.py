"""Typed payload definitions for Tally form blocks.

These payloads are primarily request-oriented and track the current block
reference used when creating or updating forms through the Tally API.

The API can still return additional payload keys on read operations, so the SDK
keeps `BlockPayload` permissive by also allowing `dict[str, Any]` as a fallback.
"""

from typing import Any, Literal, TypedDict


BadgeType = Literal["OFF", "NUMBERS", "LETTERS"]
CalculatedFieldType = Literal["NUMBER", "TEXT"]
ConditionalGroupType = Literal["SINGLE", "GROUP"]
ConditionalActionType = Literal["SHOW_BLOCKS", "HIDE_BLOCKS", "SKIP_TO"]
CurrencyCode = Literal["USD", "EUR", "GBP", "CAD", "AUD", "JPY", "CNY", "INR"]
DecimalSeparator = Literal["COMMA", "DOT"]
ThousandsSeparator = Literal["COMMA", "DOT", "SPACE", "NONE"]
NumberFormat = Literal["NUMBER", "CURRENCY", "PERCENTAGE"]
EmbedKind = Literal["rich", "video", "photo", "link", "pdf", "gist"]
DisableDay = Literal[
    "MONDAY",
    "TUESDAY",
    "WEDNESDAY",
    "THURSDAY",
    "FRIDAY",
    "SATURDAY",
    "SUNDAY",
    "PAST",
    "FUTURE",
    "TODAY",
]


class BasePayload(TypedDict, total=False):
    """Common payload fields shared by many Tally block types."""

    isHidden: bool
    columnListUuid: str
    columnUuid: str
    columnRatio: float
    name: str


class HtmlPayload(BasePayload, total=False):
    """Base payload for HTML-backed content blocks."""

    html: str


class RequiredPayload(BasePayload, total=False):
    """Base payload for required-capable question blocks."""

    isRequired: bool


class DefaultAnswerPayload(RequiredPayload, total=False):
    """Base payload for questions that support a default answer."""

    hasDefaultAnswer: bool
    defaultAnswer: Any


class PlaceholderPayload(DefaultAnswerPayload, total=False):
    """Base payload for inputs with a placeholder."""

    placeholder: str


class OrderedChoicePayload(DefaultAnswerPayload, total=False):
    """Base payload for ordered child option blocks."""

    index: int
    isFirst: bool
    isLast: bool


class DecoratedChoicePayload(OrderedChoicePayload, total=False):
    """Base payload for option blocks with color, badges, and images."""

    colorCodeOptions: bool
    color: str
    hasBadge: bool
    badgeType: BadgeType
    hasOtherOption: bool
    isOtherOption: bool
    image: str


class MentionField(TypedDict, total=False):
    """Field reference used inside a mention."""

    uuid: str
    type: Literal["INPUT_FIELD", "CALCULATED_FIELD", "HIDDEN_FIELD"]
    questionType: str
    blockGroupUuid: str
    title: str
    calculatedFieldType: CalculatedFieldType
    payload: dict[str, Any]


class Mention(TypedDict, total=False):
    """Mention object used by form title blocks."""

    uuid: str
    field: MentionField
    defaultValue: Any


class CoverSettings(TypedDict, total=False):
    """Cover display settings for a form title block."""

    objectPositionYPercent: float


class ButtonSettings(TypedDict, total=False):
    """Button settings used by supported blocks."""

    label: str


class FormTitlePayload(HtmlPayload, total=False):
    """Payload for FORM_TITLE blocks."""

    title: str
    logo: str
    cover: str
    coverSettings: CoverSettings
    mentions: list[Mention]
    button: ButtonSettings


class TextPayload(HtmlPayload, total=False):
    """Payload for TEXT blocks."""


class LabelPayload(HtmlPayload, total=False):
    """Payload for LABEL blocks."""

    isFolded: bool


class TitlePayload(HtmlPayload, total=False):
    """Payload for TITLE blocks."""

    isFolded: bool


class Heading1Payload(HtmlPayload, total=False):
    """Payload for HEADING_1 blocks."""


class Heading2Payload(HtmlPayload, total=False):
    """Payload for HEADING_2 blocks."""


class Heading3Payload(HtmlPayload, total=False):
    """Payload for HEADING_3 blocks."""


class DividerPayload(BasePayload, total=False):
    """Payload for DIVIDER blocks."""


class PageBreakPayload(BasePayload, total=False):
    """Payload for PAGE_BREAK blocks."""

    index: int
    isFirst: bool
    isLast: bool
    isQualifiedForThankYouPage: bool
    isThankYouPage: bool
    button: ButtonSettings


class ThankYouPagePayload(HtmlPayload, total=False):
    """Payload for THANK_YOU_PAGE blocks."""

    isThankYouPage: bool


class ImageSettings(TypedDict, total=False):
    """Single image descriptor for IMAGE blocks."""

    name: str
    url: str


class ImagePayload(BasePayload, total=False):
    """Payload for IMAGE blocks."""

    images: list[ImageSettings]
    caption: str
    link: str
    altText: str


class EmbedDisplay(TypedDict, total=False):
    """Display settings for EMBED blocks."""

    url: str


class EmbedPayload(BasePayload, total=False):
    """Payload for EMBED blocks."""

    type: EmbedKind
    provider: str
    title: str
    inputUrl: str
    display: EmbedDisplay
    width: str | int
    height: str | int


class EmbedVideoPayload(BasePayload, total=False):
    """Payload for EMBED_VIDEO blocks."""

    url: str
    provider: str


class EmbedAudioPayload(BasePayload, total=False):
    """Payload for EMBED_AUDIO blocks."""

    url: str
    provider: str


class QuestionPayload(RequiredPayload, total=False):
    """Payload for QUESTION blocks."""


class MatrixPayload(DefaultAnswerPayload, total=False):
    """Payload for MATRIX blocks."""


class InputTextPayload(PlaceholderPayload, total=False):
    """Payload for INPUT_TEXT blocks."""

    hasMinCharacters: bool
    minCharacters: int
    hasMaxCharacters: bool
    maxCharacters: int


class InputNumberPayload(PlaceholderPayload, total=False):
    """Payload for INPUT_NUMBER blocks."""

    hasMinValue: bool
    minValue: float
    hasMaxValue: bool
    maxValue: float
    decimalSeparator: DecimalSeparator
    thousandsSeparator: ThousandsSeparator
    numberFormat: NumberFormat
    currency: CurrencyCode


class InputEmailPayload(PlaceholderPayload, total=False):
    """Payload for INPUT_EMAIL blocks."""


class InputLinkPayload(PlaceholderPayload, total=False):
    """Payload for INPUT_LINK blocks."""


class InputPhoneNumberPayload(PlaceholderPayload, total=False):
    """Payload for INPUT_PHONE_NUMBER blocks."""


class InputDatePayload(PlaceholderPayload, total=False):
    """Payload for INPUT_DATE blocks."""

    disableDays: list[DisableDay]


class InputTimePayload(PlaceholderPayload, total=False):
    """Payload for INPUT_TIME blocks."""


class TextareaPayload(PlaceholderPayload, total=False):
    """Payload for TEXTAREA blocks."""

    hasMinCharacters: bool
    minCharacters: int
    hasMaxCharacters: bool
    maxCharacters: int


class AllowedFiles(TypedDict, total=False):
    """Allowed file categories for FILE_UPLOAD blocks."""

    images: bool
    documents: bool
    audio: bool
    video: bool
    other: bool


class FileUploadPayload(RequiredPayload, total=False):
    """Payload for FILE_UPLOAD blocks."""

    allowedFiles: AllowedFiles
    hasMaxFileSize: bool
    maxFileSize: int
    hasMaxFiles: bool
    maxFiles: int


class LinearScalePayload(DefaultAnswerPayload, total=False):
    """Payload for LINEAR_SCALE blocks."""

    minValue: int
    maxValue: int
    minLabel: str
    maxLabel: str


class RatingPayload(DefaultAnswerPayload, total=False):
    """Payload for RATING blocks."""

    maxValue: int


class HiddenField(TypedDict, total=False):
    """Single hidden field definition."""

    uuid: str
    name: str


class HiddenFieldsPayload(BasePayload, total=False):
    """Payload for HIDDEN_FIELDS blocks."""

    hiddenFields: list[HiddenField]


class MultipleChoiceOptionPayload(DecoratedChoicePayload, total=False):
    """Payload for MULTIPLE_CHOICE_OPTION blocks."""


class CheckboxPayload(RequiredPayload, total=False):
    """Payload for CHECKBOX blocks."""

    label: str
    defaultChecked: bool


class DropdownOptionPayload(OrderedChoicePayload, total=False):
    """Payload for DROPDOWN_OPTION blocks."""


class RankingOptionPayload(OrderedChoicePayload, total=False):
    """Payload for RANKING_OPTION blocks."""


class MultiSelectOptionPayload(DecoratedChoicePayload, total=False):
    """Payload for MULTI_SELECT_OPTION blocks."""


class PaymentPayload(RequiredPayload, total=False):
    """Payload for PAYMENT blocks."""

    amount: float
    currency: CurrencyCode


class SignaturePayload(RequiredPayload, total=False):
    """Payload for SIGNATURE blocks."""


class MatrixRowPayload(RequiredPayload, total=False):
    """Payload for MATRIX_ROW blocks."""

    index: int
    isFirst: bool
    isLast: bool


class MatrixColumnPayload(RequiredPayload, total=False):
    """Payload for MATRIX_COLUMN blocks."""

    index: int
    isFirst: bool
    isLast: bool


class WalletConnectPayload(RequiredPayload, total=False):
    """Payload for WALLET_CONNECT blocks."""


class Conditional(TypedDict, total=False):
    """Single conditional node in a CONDITIONAL_LOGIC block."""

    uuid: str
    type: ConditionalGroupType
    payload: dict[str, Any]


class ConditionalAction(TypedDict, total=False):
    """Single conditional action in a CONDITIONAL_LOGIC block."""

    uuid: str
    type: ConditionalActionType
    payload: dict[str, Any]


class ConditionalLogicPayload(BasePayload, total=False):
    """Payload for CONDITIONAL_LOGIC blocks."""

    conditionals: list[Conditional]
    actions: list[ConditionalAction]
    updateUuid: str
    logicalOperator: Literal["AND", "OR"]


class CalculatedField(TypedDict, total=False):
    """Single calculated field definition."""

    uuid: str
    name: str
    type: CalculatedFieldType
    value: Any


class CalculatedFieldsPayload(BasePayload, total=False):
    """Payload for CALCULATED_FIELDS blocks."""

    fields: list[CalculatedField]
    formula: str


class CaptchaPayload(RequiredPayload, total=False):
    """Payload for CAPTCHA blocks."""

    provider: str


class RespondentCountryPayload(RequiredPayload, total=False):
    """Payload for RESPONDENT_COUNTRY blocks."""


class OptionPayload(BasePayload, total=False):
    """Generic option payload kept as a compatibility escape hatch."""

    label: str
    value: str
    text: str


BlockPayload = (
    FormTitlePayload
    | TextPayload
    | LabelPayload
    | TitlePayload
    | Heading1Payload
    | Heading2Payload
    | Heading3Payload
    | DividerPayload
    | PageBreakPayload
    | ThankYouPagePayload
    | ImagePayload
    | EmbedPayload
    | EmbedVideoPayload
    | EmbedAudioPayload
    | QuestionPayload
    | MatrixPayload
    | InputTextPayload
    | InputNumberPayload
    | InputEmailPayload
    | InputLinkPayload
    | InputPhoneNumberPayload
    | InputDatePayload
    | InputTimePayload
    | TextareaPayload
    | FileUploadPayload
    | LinearScalePayload
    | RatingPayload
    | HiddenFieldsPayload
    | MultipleChoiceOptionPayload
    | CheckboxPayload
    | DropdownOptionPayload
    | RankingOptionPayload
    | MultiSelectOptionPayload
    | OptionPayload
    | PaymentPayload
    | SignaturePayload
    | MatrixRowPayload
    | MatrixColumnPayload
    | WalletConnectPayload
    | ConditionalLogicPayload
    | CalculatedFieldsPayload
    | CaptchaPayload
    | RespondentCountryPayload
    | dict[str, Any]
)


__all__ = [
    "AllowedFiles",
    "BasePayload",
    "BlockPayload",
    "ButtonSettings",
    "CalculatedField",
    "CalculatedFieldsPayload",
    "CaptchaPayload",
    "CheckboxPayload",
    "Conditional",
    "ConditionalAction",
    "ConditionalLogicPayload",
    "CoverSettings",
    "DividerPayload",
    "DropdownOptionPayload",
    "EmbedAudioPayload",
    "EmbedDisplay",
    "EmbedPayload",
    "EmbedVideoPayload",
    "FileUploadPayload",
    "FormTitlePayload",
    "Heading1Payload",
    "Heading2Payload",
    "Heading3Payload",
    "HiddenField",
    "HiddenFieldsPayload",
    "ImagePayload",
    "ImageSettings",
    "InputDatePayload",
    "InputEmailPayload",
    "InputLinkPayload",
    "InputNumberPayload",
    "InputPhoneNumberPayload",
    "InputTextPayload",
    "InputTimePayload",
    "LabelPayload",
    "LinearScalePayload",
    "MatrixColumnPayload",
    "MatrixPayload",
    "MatrixRowPayload",
    "Mention",
    "MentionField",
    "MultiSelectOptionPayload",
    "MultipleChoiceOptionPayload",
    "OptionPayload",
    "PageBreakPayload",
    "PaymentPayload",
    "QuestionPayload",
    "RankingOptionPayload",
    "RatingPayload",
    "RespondentCountryPayload",
    "SignaturePayload",
    "TextPayload",
    "TextareaPayload",
    "ThankYouPagePayload",
    "TitlePayload",
    "WalletConnectPayload",
]

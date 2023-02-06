import enum


class AccountType(enum.Enum):
    MAIN = 'MAIN'


class AccountTransactionOperationType(enum.Enum):
    INCREMENT = 'INCREMENT'
    # Может привести к отрицательному балансу счёта
    DECREMENT = 'DECREMENT'
    # Не позволяет снять средства при недостаточном размере счёта
    DECREMENT_SAFE = 'DECREMENT_SAFE'
    # "Погашение", при счёте 100 и размере операции 200 на счету будет 0
    DECREMENT_ZERO = 'DECREMENT_ZERO'

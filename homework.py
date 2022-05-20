from typing import List, Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Информация о тренировке"""
        REPORT_MESSAGE = (
            'Тип тренировки: {tr_type}; \n'
            'Длительность: {dur:.3f} ч.; \n'
            'Дистанция: {dis:.3f} км; \n'
            'Ср. скорость: {sp:.3f} км/ч; \n'
            'Потрачено ккал: {cal:.3f}.'
        )
        return REPORT_MESSAGE.format(
            tr_type=self.training_type,
            dur=self.duration,
            dis=self.distance,
            sp=self.speed,
            cal=self.calories
        )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65  # Зависит от типа тренировки.
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            (self.action * self.LEN_STEP / self.M_IN_KM) / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    COEF_CAL_RUN_1 = 18
    COEF_CAL_RUN_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEF_CAL_RUN_1 * self.get_mean_speed()
                - self.COEF_CAL_RUN_2)
                * self.weight / self.M_IN_KM * self.duration
                * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_CAL_WLK_1 = 0.035
    COEF_CAL_WLK_2 = 2
    COEF_CAL_WLK_3 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        # Формула расчета расхода калорий для спортивной ходьбы.
        return (
            (self.COEF_CAL_WLK_1 * self.weight
                + (self.get_mean_speed()**self.COEF_CAL_WLK_2
                    // self.height)
                * self.COEF_CAL_WLK_3
                * self.weight) * self.duration * self.MIN_IN_HOUR
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEF_CAL_SWM_1: float = 1.1
    COEF_CAL_SWM_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при пллавании."""
        # Формула расчета расхода калорий для плавания.
        return (
            (self.get_mean_speed()
             + self.COEF_CAL_SWM_1) * self.COEF_CAL_SWM_2 * self.weight
        )

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        return (
            (self.length_pool
             * self.count_pool) / self.M_IN_KM / self.duration
        )


def read_package(workout_type: Dict[str, Type[Training]], data: List[int]):
    """Прочитать данные полученные от датчиков."""
    workout_types = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    if workout_type in workout_types:
        return workout_types[workout_type](*data)
    elif KeyError:
        print('Тренировка не найдена')


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

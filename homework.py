
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

    def show_training_info(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')

    def get_messagae(self) -> str:
        """Информация о тренировке"""
        pass


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = (self.action * self.LEN_STEP / self.M_IN_KM) / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""

    coeff_calorie_r_1 = 18
    coeff_calorie_r_2 = 20
    M_IN_KM: int = 1000

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.coeff_calorie_r_1 * self.get_mean_speed()
                    - self.coeff_calorie_r_2)
                    * self.weight / self.M_IN_KM * self.duration)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    coeff_cal_w_1 = 0.035
    coe_cal_w_2 = 2
    coeff_cal_w_3 = 0.029

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
        calories = ((self.coeff_cal_w_1 * self.weight
                    + (self.get_mean_speed()**self.coe_cal_w_2 // self.height)
                    * self.coeff_cal_w_3 * self.weight) * self.duration)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    coeff_calorie_s_1: float = 1.1
    coeff_calorie_s_2: float = 2

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
        calories = ((self.get_mean_speed() + self.coeff_calorie_s_1)
                    * self.coeff_calorie_s_2 * self.weight)
        return calories

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        speed = ((self.length_pool * self.count_pool)
                 / self.M_IN_KM / self.duration)
        return speed


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info().get_message()
    return print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

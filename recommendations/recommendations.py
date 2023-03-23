# recommendations/recommendations.py

from concurrent import futures
import random


import grpc

from recommendations_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationResponse,
)

import recommendations_pb2_grpc

books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="Мальтийский сокол"),
        BookRecommendation(id=2, title="Убийство в Восточном экспрессе"),
        BookRecommendation(id=3, title="Собака Баскервилей"),
        BookRecommendation(id=4, title="Автостопом по галактике"),
        BookRecommendation(id=5, title="Игра Эндера"),
        BookRecommendation(id=6, title="Зелёная миля"),
        BookRecommendation(id=7, title="Женщина в чёрном"),
        BookRecommendation(id=8, title="Костяная кукла"),
        BookRecommendation(id=9, title="Мэйфейрские ведьмы"),
        BookRecommendation(id=10, title="Тёмная половина"),
    ],

    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(id=11, title="Дюна"),
        BookRecommendation(id=12, title="Властелин колец"),
        BookRecommendation(id=13, title="Академия"),
        BookRecommendation(id=14, title="Чужак в чужой стране"),
        BookRecommendation(id=15, title="Нейромант"),
        BookRecommendation(id=16, title="Туманы Авалона"),
        BookRecommendation(id=17, title="451° по Фаренгейту"),
        BookRecommendation(id=18, title="И явилось Новое Солнце"),
        BookRecommendation(id=19, title="Стальные пещеры"),
        BookRecommendation(id=20, title="Дети атома"),

    ],

    BookCategory.SELF_HELP: [
        BookRecommendation(id=21, title="Семь навыков высокоэффективных людей"),
        BookRecommendation(id=22, title="Как завоёвывать друзей и оказыватьвлияние на людей"),
        BookRecommendation(id=23, title="Человек в поисках смысла"),
        BookRecommendation(id=24, title="Богатый папа, бедный папа"),
        BookRecommendation(id=25, title="Тайм-драйв. Как успевать жить и работать"),
        BookRecommendation(id=26, title="Супермышление"),
        BookRecommendation(id=27, title="Марс и Венера. Ключ к личному успеху"),
        BookRecommendation(id=28, title="Великолепный мозг в любом возрасте"),
        BookRecommendation(id=29, title="Приручение страха"),
        BookRecommendation(id=30, title="Как стать несчастным без посторонней помощи"),
    ],
}
class RecommendationService(
    recommendations_pb2_grpc.RecommendationsServicer
):

    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(
            books_for_category, num_results
        )

        return RecommendationResponse(recommendations=books_to_recommend)
        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()


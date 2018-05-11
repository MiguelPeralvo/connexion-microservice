import os
import connexion

from injector import Binder
from flask_injector import FlaskInjector
from connexion.resolver import RestyResolver

from services.elasticsearch import ElasticSearchIndex, ElasticSearchFactory
from conf.elasticsearch_mapper import room_mapping
import logging
import graypy
#from services.provider import ItemsProvider


# def configure(binder: Binder) -> Binder:
#     binder.bind(
#         ItemsProvider,
#         ItemsProvider([{"Name": "Test 1"}])
#     )


def configure(binder: Binder) -> Binder:
  binder.bind(
    ElasticSearchIndex,
    ElasticSearchIndex(
      ElasticSearchFactory(
          os.environ['ELASTICSEARCH_HOST'],
          os.environ['ELASTICSEARCH_PORT'],
      ),
      'rooms',
      'room',
      room_mapping
    )
  )

  return binder


if __name__ == '__main__':
  # logging.basicConfig(level=logging.INFO, filename='app.log')
  app = connexion.App(__name__, specification_dir='swagger/')
  app.add_api('indexer.yaml', resolver=RestyResolver('api'))
  FlaskInjector(app=app.app, modules=[configure])
  handler = graypy.GELFHandler(os.environ['GRAYLOG_HOST'], int(os.environ['GRAYLOG_PORT']))
  # app.logger.addHandler(handler)
  logger = logging.getLogger('app')
  logger.setLevel(logging.INFO)
  logger.addHandler(handler)
  app.run(port=9090)

# if __name__ == '__main__':
#     app = connexion.App(__name__, specification_dir='swagger/')
#     app.add_api('app.yaml', resolver=RestyResolver('api'))
#     FlaskInjector(app=app.app, modules=[configure])
#     app.run(port=9090)
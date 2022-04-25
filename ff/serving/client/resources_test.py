# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

#
import pytest
from resources import ResourceRedefinedError, ResourceState, Provider, RedisConfig, SnowflakeConfig, PostgresConfig, User, Provider, Entity, Feature, Label, TrainingSet, PrimaryData, SQLTable, Source


@pytest.fixture
def postgres_config():
    return PostgresConfig(
        host="localhost",
        port=123,
        database="db",
        user="user",
        password="p4ssw0rd",
    )


@pytest.fixture
def snowflake_config():
    return SnowflakeConfig(
        account="act",
        database="db",
        organization="org",
        username="user",
        password="pwd",
        schema="schema",
    )


@pytest.fixture
def redis_config():
    return RedisConfig(
        host="localhost",
        port=123,
        password="abc",
        db=3,
    )


@pytest.fixture
def postgres_provider(postgres_config):
    return Provider(
        name="postgres",
        description="desc2",
        function="fn2",
        team="team2",
        config=postgres_config,
    )


@pytest.fixture
def snowflake_provider(snowflake_config):
    return Provider(
        name="snowflake",
        description="desc3",
        function="fn3",
        team="team3",
        config=snowflake_config,
    )


@pytest.fixture
def redis_provider(redis_config):
    return Provider(
        name="redis",
        description="desc3",
        function="fn3",
        team="team3",
        config=redis_config,
    )


@pytest.fixture
def all_resources_set(redis_provider):
    return [
        redis_provider,
        User(name="Featureform"),
        Entity(name="user", description="A user"),
        Source(name="primary",
               variant="abc",
               definition=PrimaryData(location=SQLTable("table")),
               owner="someone",
               description="desc",
               provider="redis-name"),
        Feature(name="feature",
                variant="v1",
                description="feature",
                t="float32",
                entity="user",
                owner="Owner",
                provider="redis-name"),
        Label(name="label",
              variant="v1",
              description="feature",
              t="float32",
              entity="user",
              owner="Owner",
              provider="redis-name"),
        TrainingSet(name="training-set",
                    variant="v1",
                    description="desc",
                    owner="featureform",
                    provider="redis-name",
                    label=("label", "var"),
                    features=[("f1", "var")]),
    ]


@pytest.fixture
def all_resources_strange_order(redis_provider):
    return [
        TrainingSet(name="training-set",
                    variant="v1",
                    description="desc",
                    owner="featureform",
                    provider="redis-name",
                    label=("label", "var"),
                    features=[("f1", "var")]),
        Label(name="label",
              variant="v1",
              description="feature",
              t="float32",
              entity="user",
              owner="Owner",
              provider="redis-name"),
        Feature(name="feature",
                variant="v1",
                description="feature",
                t="float32",
                entity="user",
                owner="Owner",
                provider="redis-name"),
        Entity(name="user", description="A user"),
        Source(name="primary",
               variant="abc",
               definition=PrimaryData(location=SQLTable("table")),
               owner="someone",
               description="desc",
               provider="redis-name"),
        redis_provider,
        User(name="Featureform"),
    ]


def test_create_all_provider_types(redis_provider, snowflake_provider,
                                   postgres_provider):
    providers = [
        redis_provider,
        snowflake_provider,
        postgres_provider,
    ]
    state = ResourceState()
    for provider in providers:
        state.add(provider)


def test_redefine_provider(redis_config, snowflake_config):
    providers = [
        Provider(name="name",
                 description="desc",
                 function="fn",
                 team="team",
                 config=redis_config),
        Provider(name="name",
                 description="desc2",
                 function="fn2",
                 team="team2",
                 config=snowflake_config),
    ]
    state = ResourceState()
    state.add(providers[0])
    with pytest.raises(ResourceRedefinedError):
        state.add(providers[1])


def test_add_all_resource_types(all_resources_strange_order, redis_config):
    state = ResourceState()
    for resource in all_resources_strange_order:
        state.add(resource)
    assert state.sorted_list() == [
        User(name="Featureform"),
        Provider(
            name="redis",
            description="desc3",
            function="fn3",
            team="team3",
            config=redis_config,
        ),
        Source(name="primary",
               variant="abc",
               definition=PrimaryData(location=SQLTable("table")),
               owner="someone",
               description="desc",
               provider="redis-name"),
        Entity(name="user", description="A user"),
        Feature(name="feature",
                variant="v1",
                description="feature",
                t="float32",
                entity="user",
                owner="Owner",
                provider="redis-name"),
        Label(name="label",
              variant="v1",
              description="feature",
              t="float32",
              entity="user",
              owner="Owner",
              provider="redis-name"),
        TrainingSet(name="training-set",
                    variant="v1",
                    description="desc",
                    owner="featureform",
                    provider="redis-name",
                    label=("label", "var"),
                    features=[("f1", "var")]),
    ]


def test_resource_types_differ(all_resources_set):
    types = set()
    for resource in all_resources_set:
        t = resource.type()
        assert t not in types
        types.add(t)


def test_invalid_providers(snowflake_config):
    provider_args = [
        {
            "description": "desc",
            "function": "fn",
            "team": "team",
            "config": snowflake_config
        },
        {
            "name": "name",
            "description": "desc",
            "team": "team",
            "config": snowflake_config
        },
        {
            "name": "name",
            "description": "desc",
            "function": "fn",
            "team": "team"
        },
    ]
    for args in provider_args:
        with pytest.raises(TypeError):
            Provider(**args)


def test_invalid_users():
    user_args = [{}]
    for args in user_args:
        with pytest.raises(TypeError):
            User(**args)


@pytest.mark.parametrize("args", [
    {
        "name": "name",
        "variant": "var",
        "owner": "featureform",
        "provider": "offline_store",
        "description": "abc",
        "label": ("var"),
        "features": [("a", "var")],
    },
    {
        "name": "name",
        "variant": "var",
        "owner": "featureform",
        "provider": "offline_store",
        "label": ("", "var"),
        "description": "abc",
        "features": [("a", "var")],
    },
    {
        "name": "name",
        "variant": "var",
        "owner": "featureform",
        "provider": "offline_store",
        "label": ("a", "var"),
        "features": [],
        "description": "abc",
    },
    {
        "name": "name",
        "variant": "var",
        "owner": "featureform",
        "provider": "offline_store",
        "label": ("a", "var"),
        "features": [("a", "var"), ("var")],
        "description": "abc",
    },
    {
        "name": "name",
        "variant": "var",
        "owner": "featureform",
        "provider": "offline_store",
        "label": ("a", "var"),
        "features": [("a", "var"), ("", "var")],
        "description": "abc",
    },
    {
        "name": "name",
        "variant": "var",
        "owner": "featureform",
        "provider": "offline_store",
        "label": ("a", "var"),
        "features": [("a", "var"), ("b", "")],
        "description": "abc",
    },
])
def test_invalid_training_set(args):
    with pytest.raises((ValueError, TypeError)):
        TrainingSet(**args)
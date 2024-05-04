{- Main configuration file for bffh
 - ================================
 -
 - In this configuration file you configure almost all parts of how bffh operates, but most importantly:
 -      * Machines
 -      * Initiators and Actors
 -      * Which Initiators and Actors relate to which machine(s)
 -      * Roles and the permissions granted by them
 -}

-- The config is in the configuration format/language dhall. You can find more information about dhall over at
-- https://dhall-lang.org

-- (Our) Dhall is somewhat similar to JSON and YAML in that it expects a top-level object containing the
-- configuration values
{
    -- Configure the addresses and ports bffh listens on
    listens = [
        -- BFFH binds a port for every listen object in this array.
        -- Each listen object is of the format { address = <STRING>, port = <INTEGER> }
        -- If you don't specify a port bffh will use the default of `59661`
        -- 'address' can be a IP address or a hostname
        -- If bffh can not bind a port for the specified combination if will log an error but *continue with the remaining ports*
        { address = "127.0.0.1", port = 59661 },
        { address = "::1", port = 59661 },
        { address = "steak.fritz.box", port = 59661 }
    ],

    -- Configure TLS. BFFH requires a PEM-encoded certificate and the associated key as two separate files
    certfile = "examples/self-signed-cert.pem",
    keyfile = "examples/self-signed-key.pem",

    -- BFFH right now requires a running MQTT broker.
    mqtt_url = "tcp://localhost:1883",

    -- Path to the database file for bffh. bffh will in fact create two files; ${db_path} and ${db_path}.lock.
    -- BFFH will *not* create any directories so ensure that the directory exists and the user running bffh has write
    -- access into them.
    db_path = "/tmp/bffh",

    -- Audit log path. Bffh will log state changes into this file, one per line.
    -- Audit log entries are for now JSON:
    -- {"timestamp":1641497361,"machine":"Testmachine","state":{"state":{"InUse":{"uid":"Testuser","subuid":null,"realm":null}}}}
    auditlog_path = "/tmp/bffh.audit",


    -- ||| GENERATOR START
    -- ||| GENERATOR END


    -- Initiators are configured almost the same way as Actors, refer to actor documentation for more details
    -- The below '{=}' is what you need if you want to define *no* initiators at all and only use the API with apps
    -- to let people use machines.
    initiators = {=},
    -- The "Dummy" initiator will try to use and return a machine as the given user every few seconds. It's good to
    -- test your system but will spam your log so is disabled by default.
    --initiators = { Initiator = { module = "Dummy", params = { uid = "Testuser" } } },

    -- Linking up machines to initiators. Similar to actors a machine can have several initiators assigned but an
    -- initiator can only be assigned to one machine.
    -- The below is once again how you have to define *no* initiators.
    init_connections = [] : List { machine : Text, initiator : Text },
    --init_connections = [{ machine = "Testmachine", initiator = "Initiator" }]

    instanceurl = "https://example.com",
    spacename = "examplespace"
}

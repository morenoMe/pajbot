import logging

log = logging.getLogger('tyggbot')

"""
This function will handle all database changes

TODO: Also let it create all tables if none exist.
"""
def update_database(sqlconn):
    cursor = sqlconn.cursor()

    cursor.execute("SELECT `value` FROM `tb_settings` WHERE `setting`='db_version'")
    log.info(cursor)

    latest_db_version = 2
    version = 0

    if cursor.rowcount > 0:
        # No db version specified
        version = int(cursor.fetchone()[0])
    else:
        cursor.execute("INSERT INTO `tb_settings` (`setting`, `value`, `type`) VALUES ('db_version', 0, 'int')")

    while version < latest_db_version:
        version += 1
        queries = []

        if version == 1:
            queries.append("ALTER TABLE `tb_user` ADD `subscriber` BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'Keeps track of whether the user is a subscriber or not. This is only updated when the user actually types in chat, so the information might be outdated if the person stops typing in chat.' ;")
        elif version == 2:
            queries.append("CREATE TABLE `tb_emote` ( `id` INT NOT NULL AUTO_INCREMENT , `code` VARCHAR(64) NOT NULL COMMENT 'All regexes for emotes are escaped. so if the emote code is (ditto) the regex will be \\(ditto\\)' , `deque` TEXT NULL DEFAULT NULL COMMENT 'Dump of the emote deque, so the state can be saved properly' , `pm_record` INT NOT NULL DEFAULT '0' , `tm_record` INT NOT NULL DEFAULT '0' , `count` INT NOT NULL DEFAULT '0', PRIMARY KEY (`id`) ) ENGINE = InnoDB;");

        for query in queries:
            cursor.execute(query)

        log.info('Updating db version to {0}'.format(version))
        cursor.execute("UPDATE `tb_settings` SET `value`=%s WHERE `setting`='db_version'", (version))

    log.info('db version: {0}'.format(version))
BEGIN TRANSACTION;
CREATE TABLE "auth_permission" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "content_type_id" integer NOT NULL,
    "codename" varchar(100) NOT NULL,
    UNIQUE ("content_type_id", "codename")
);
INSERT INTO "auth_permission" VALUES(1,'Can add permission',1,'add_permission');
INSERT INTO "auth_permission" VALUES(2,'Can change permission',1,'change_permission');
INSERT INTO "auth_permission" VALUES(3,'Can delete permission',1,'delete_permission');
INSERT INTO "auth_permission" VALUES(4,'Can add group',2,'add_group');
INSERT INTO "auth_permission" VALUES(5,'Can change group',2,'change_group');
INSERT INTO "auth_permission" VALUES(6,'Can delete group',2,'delete_group');
INSERT INTO "auth_permission" VALUES(7,'Can add user',3,'add_user');
INSERT INTO "auth_permission" VALUES(8,'Can change user',3,'change_user');
INSERT INTO "auth_permission" VALUES(9,'Can delete user',3,'delete_user');
INSERT INTO "auth_permission" VALUES(10,'Can add message',4,'add_message');
INSERT INTO "auth_permission" VALUES(11,'Can change message',4,'change_message');
INSERT INTO "auth_permission" VALUES(12,'Can delete message',4,'delete_message');
INSERT INTO "auth_permission" VALUES(13,'Can add content type',5,'add_contenttype');
INSERT INTO "auth_permission" VALUES(14,'Can change content type',5,'change_contenttype');
INSERT INTO "auth_permission" VALUES(15,'Can delete content type',5,'delete_contenttype');
INSERT INTO "auth_permission" VALUES(16,'Can add session',6,'add_session');
INSERT INTO "auth_permission" VALUES(17,'Can change session',6,'change_session');
INSERT INTO "auth_permission" VALUES(18,'Can delete session',6,'delete_session');
INSERT INTO "auth_permission" VALUES(19,'Can add site',7,'add_site');
INSERT INTO "auth_permission" VALUES(20,'Can change site',7,'change_site');
INSERT INTO "auth_permission" VALUES(21,'Can delete site',7,'delete_site');
INSERT INTO "auth_permission" VALUES(22,'Can add language',8,'add_language');
INSERT INTO "auth_permission" VALUES(23,'Can change language',8,'change_language');
INSERT INTO "auth_permission" VALUES(24,'Can delete language',8,'delete_language');
INSERT INTO "auth_permission" VALUES(25,'Can add group',9,'add_group');
INSERT INTO "auth_permission" VALUES(26,'Can change group',9,'change_group');
INSERT INTO "auth_permission" VALUES(27,'Can delete group',9,'delete_group');
INSERT INTO "auth_permission" VALUES(28,'Can add translation',10,'add_translation');
INSERT INTO "auth_permission" VALUES(29,'Can change translation',10,'change_translation');
INSERT INTO "auth_permission" VALUES(30,'Can delete translation',10,'delete_translation');
INSERT INTO "auth_permission" VALUES(31,'Can add log entry',11,'add_logentry');
INSERT INTO "auth_permission" VALUES(32,'Can change log entry',11,'change_logentry');
INSERT INTO "auth_permission" VALUES(33,'Can delete log entry',11,'delete_logentry');
INSERT INTO "auth_permission" VALUES(34,'Can add communicator',12,'add_communicator');
INSERT INTO "auth_permission" VALUES(35,'Can change communicator',12,'change_communicator');
INSERT INTO "auth_permission" VALUES(36,'Can delete communicator',12,'delete_communicator');
INSERT INTO "auth_permission" VALUES(37,'Can add balancer',13,'add_balancer');
INSERT INTO "auth_permission" VALUES(38,'Can change balancer',13,'change_balancer');
INSERT INTO "auth_permission" VALUES(39,'Can delete balancer',13,'delete_balancer');
INSERT INTO "auth_permission" VALUES(40,'Can add division user',14,'add_divisionuser');
INSERT INTO "auth_permission" VALUES(41,'Can change division user',14,'change_divisionuser');
INSERT INTO "auth_permission" VALUES(42,'Can delete division user',14,'delete_divisionuser');
INSERT INTO "auth_permission" VALUES(43,'Can add position user',15,'add_positionuser');
INSERT INTO "auth_permission" VALUES(44,'Can change position user',15,'change_positionuser');
INSERT INTO "auth_permission" VALUES(45,'Can delete position user',15,'delete_positionuser');
INSERT INTO "auth_permission" VALUES(46,'Can add status user',16,'add_statususer');
INSERT INTO "auth_permission" VALUES(47,'Can change status user',16,'change_statususer');
INSERT INTO "auth_permission" VALUES(48,'Can delete status user',16,'delete_statususer');
INSERT INTO "auth_permission" VALUES(49,'Can add kpp',17,'add_kpp');
INSERT INTO "auth_permission" VALUES(50,'Can change kpp',17,'change_kpp');
INSERT INTO "auth_permission" VALUES(51,'Can delete kpp',17,'delete_kpp');
INSERT INTO "auth_permission" VALUES(52,'Can add document',18,'add_document');
INSERT INTO "auth_permission" VALUES(53,'Can change document',18,'change_document');
INSERT INTO "auth_permission" VALUES(54,'Can delete document',18,'delete_document');
INSERT INTO "auth_permission" VALUES(55,'Can add category',19,'add_category');
INSERT INTO "auth_permission" VALUES(56,'Can change category',19,'change_category');
INSERT INTO "auth_permission" VALUES(57,'Can delete category',19,'delete_category');
INSERT INTO "auth_permission" VALUES(58,'Can add user',20,'add_user');
INSERT INTO "auth_permission" VALUES(59,'Can change user',20,'change_user');
INSERT INTO "auth_permission" VALUES(60,'Can delete user',20,'delete_user');
INSERT INTO "auth_permission" VALUES(61,'Can add login journal',21,'add_loginjournal');
INSERT INTO "auth_permission" VALUES(62,'Can change login journal',21,'change_loginjournal');
INSERT INTO "auth_permission" VALUES(63,'Can delete login journal',21,'delete_loginjournal');
INSERT INTO "auth_permission" VALUES(64,'Can add group person',22,'add_groupperson');
INSERT INTO "auth_permission" VALUES(65,'Can change group person',22,'change_groupperson');
INSERT INTO "auth_permission" VALUES(66,'Can delete group person',22,'delete_groupperson');
INSERT INTO "auth_permission" VALUES(67,'Can add person',23,'add_person');
INSERT INTO "auth_permission" VALUES(68,'Can change person',23,'change_person');
INSERT INTO "auth_permission" VALUES(69,'Can delete person',23,'delete_person');
INSERT INTO "auth_permission" VALUES(70,'Can add person id',24,'add_personid');
INSERT INTO "auth_permission" VALUES(71,'Can change person id',24,'change_personid');
INSERT INTO "auth_permission" VALUES(72,'Can delete person id',24,'delete_personid');
INSERT INTO "auth_permission" VALUES(73,'Can add Роль',25,'add_rule');
INSERT INTO "auth_permission" VALUES(74,'Can change Роль',25,'change_rule');
INSERT INTO "auth_permission" VALUES(75,'Can delete Роль',25,'delete_rule');
INSERT INTO "auth_permission" VALUES(76,'Can add rule group',26,'add_rulegroup');
INSERT INTO "auth_permission" VALUES(77,'Can change rule group',26,'change_rulegroup');
INSERT INTO "auth_permission" VALUES(78,'Can delete rule group',26,'delete_rulegroup');
INSERT INTO "auth_permission" VALUES(79,'Can add camera',27,'add_camera');
INSERT INTO "auth_permission" VALUES(80,'Can change camera',27,'change_camera');
INSERT INTO "auth_permission" VALUES(81,'Can delete camera',27,'delete_camera');
INSERT INTO "auth_permission" VALUES(82,'Can add journal',28,'add_journal');
INSERT INTO "auth_permission" VALUES(83,'Can change journal',28,'change_journal');
INSERT INTO "auth_permission" VALUES(84,'Can delete journal',28,'delete_journal');
INSERT INTO "auth_permission" VALUES(85,'Can add default params',29,'add_defaultparams');
INSERT INTO "auth_permission" VALUES(86,'Can change default params',29,'change_defaultparams');
INSERT INTO "auth_permission" VALUES(87,'Can delete default params',29,'delete_defaultparams');
INSERT INTO "auth_permission" VALUES(88,'Can add ground',30,'add_ground');
INSERT INTO "auth_permission" VALUES(89,'Can change ground',30,'change_ground');
INSERT INTO "auth_permission" VALUES(90,'Can delete ground',30,'delete_ground');
INSERT INTO "auth_permission" VALUES(91,'Can add visiting card',31,'add_visitingcard');
INSERT INTO "auth_permission" VALUES(92,'Can change visiting card',31,'change_visitingcard');
INSERT INTO "auth_permission" VALUES(93,'Can delete visiting card',31,'delete_visitingcard');
INSERT INTO "auth_permission" VALUES(94,'Can add positions status',32,'add_positionsstatus');
INSERT INTO "auth_permission" VALUES(95,'Can change positions status',32,'change_positionsstatus');
INSERT INTO "auth_permission" VALUES(96,'Can delete positions status',32,'delete_positionsstatus');
CREATE TABLE "auth_group_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("group_id", "permission_id")
);
CREATE TABLE "auth_group" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(80) NOT NULL UNIQUE
);
CREATE TABLE "auth_user_user_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("user_id", "permission_id")
);
CREATE TABLE "auth_user_groups" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id"),
    UNIQUE ("user_id", "group_id")
);
CREATE TABLE "auth_user" (
    "id" integer NOT NULL PRIMARY KEY,
    "username" varchar(30) NOT NULL UNIQUE,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "email" varchar(75) NOT NULL,
    "password" varchar(128) NOT NULL,
    "is_staff" bool NOT NULL,
    "is_active" bool NOT NULL,
    "is_superuser" bool NOT NULL,
    "last_login" datetime NOT NULL,
    "date_joined" datetime NOT NULL
);
INSERT INTO "auth_user" VALUES(1,'admin','','','admin@admin.ru','sha1$84422$679cd5e532ca70caf9607bc78c9e15b40c974d4d',1,1,1,'2010-11-15 19:53:24.974193','2010-10-15 13:12:13.095584');
INSERT INTO "auth_user" VALUES(2,'dima','','','','sha1$5be8a$9fc1923a0c6975a0ed60a7f9a6da919f84901dbe',1,1,0,'2010-11-13 22:34:50.222168','2010-11-13 19:19:18.228929');
INSERT INTO "auth_user" VALUES(3,'serg','','','','sha1$8ab38$b8cc95a4f20f46f2b8a13c2791fce5a2dfb4a967',1,1,0,'2010-11-13 20:37:46.141097','2010-11-13 20:20:30.235980');
INSERT INTO "auth_user" VALUES(4,'julia','','','','sha1$8f3c2$6cd469b297a053b2824fdc8fe25741b4a752958c',1,1,0,'2010-11-15 15:02:17.514435','2010-11-15 15:02:17.514446');
INSERT INTO "auth_user" VALUES(5,'123','','','','sha1$b6b2a$5123cb5fe16a45bac79f5397ff21cb51cd13a6cf',1,1,0,'2010-11-15 15:02:35.310610','2010-11-15 15:02:35.310617');
INSERT INTO "auth_user" VALUES(6,'ss','','','','sha1$b0119$b87e1fec8f8a985879bfbc92f31f0bd09483f583',1,1,0,'2010-11-15 15:03:16.249032','2010-11-15 15:03:16.249040');
INSERT INTO "auth_user" VALUES(7,'1','','','','sha1$2ab99$229d4c1742d8399e7fd10dd5c95362681118f940',1,1,0,'2010-11-15 15:03:30.979114','2010-11-15 15:03:30.979123');
INSERT INTO "auth_user" VALUES(8,'2','','','','sha1$d9c64$9b735bee4a8d7bb6b72ffb51dc6a865aea3148e6',1,1,0,'2010-11-15 15:03:42.783279','2010-11-15 15:03:42.783290');
INSERT INTO "auth_user" VALUES(9,'3','','','','sha1$8f679$2b2b9fe76eae10a1c3b9adee328cb8ebe9a54ace',1,1,0,'2010-11-15 15:03:52.267148','2010-11-15 15:03:52.267159');
INSERT INTO "auth_user" VALUES(10,'4','','','','sha1$46e95$bbc6caa8af88bc4ffdb75ac75c90d734f3feb880',1,1,0,'2010-11-15 15:04:05.179442','2010-11-15 15:04:05.179450');
INSERT INTO "auth_user" VALUES(11,'5','','','','sha1$96cba$61a042b24d2200d42f68e41e6cd2eb8613c787d3',1,1,0,'2010-11-15 15:04:18.595429','2010-11-15 15:04:18.595440');
INSERT INTO "auth_user" VALUES(12,'6','','','','sha1$f377b$2dc70f82a9bef3375218e53cd0a86951ed2a0326',1,1,0,'2010-11-15 15:04:29.864577','2010-11-15 15:04:29.864591');
INSERT INTO "auth_user" VALUES(13,'7','','','','sha1$a1fc0$172e22756547c3c5bc367c277a7a6b2f3da31932',1,1,0,'2010-11-15 15:04:42.903240','2010-11-15 15:04:42.903248');
INSERT INTO "auth_user" VALUES(14,'8','','','','sha1$36082$1be2c85ce02b96d20b88da4148bcbb444d25bbb4',1,1,0,'2010-11-15 15:04:54.116139','2010-11-15 15:04:54.116151');
INSERT INTO "auth_user" VALUES(15,'9','','','','sha1$6def6$41287a1f8395e1214876492a7d3e504c0f7637a7',1,1,0,'2010-11-15 15:05:41.920641','2010-11-15 15:05:41.920652');
INSERT INTO "auth_user" VALUES(16,'10','','','','sha1$fbe9b$36c93260df2f23df161662dd16f86b653f92c0ee',1,1,0,'2010-11-15 15:05:57.554497','2010-11-15 15:05:57.554513');
INSERT INTO "auth_user" VALUES(17,'11','','','','sha1$d5315$0127cbd7c2db5cf80c2bda10d045f6303b6259f5',1,1,0,'2010-11-15 15:06:10.927436','2010-11-15 15:06:10.927443');
CREATE TABLE "auth_message" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "message" text NOT NULL
);
CREATE TABLE "django_content_type" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "app_label" varchar(100) NOT NULL,
    "model" varchar(100) NOT NULL,
    UNIQUE ("app_label", "model")
);
INSERT INTO "django_content_type" VALUES(1,'permission','auth','permission');
INSERT INTO "django_content_type" VALUES(2,'group','auth','group');
INSERT INTO "django_content_type" VALUES(3,'user','auth','user');
INSERT INTO "django_content_type" VALUES(4,'message','auth','message');
INSERT INTO "django_content_type" VALUES(5,'content type','contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES(6,'session','sessions','session');
INSERT INTO "django_content_type" VALUES(7,'site','sites','site');
INSERT INTO "django_content_type" VALUES(8,'language','videoclient','language');
INSERT INTO "django_content_type" VALUES(9,'group','videoclient','group');
INSERT INTO "django_content_type" VALUES(10,'translation','videoclient','translation');
INSERT INTO "django_content_type" VALUES(11,'log entry','admin','logentry');
INSERT INTO "django_content_type" VALUES(12,'communicator','videoclient','communicator');
INSERT INTO "django_content_type" VALUES(13,'balancer','videoclient','balancer');
INSERT INTO "django_content_type" VALUES(14,'division user','videoclient','divisionuser');
INSERT INTO "django_content_type" VALUES(15,'position user','videoclient','positionuser');
INSERT INTO "django_content_type" VALUES(16,'status user','videoclient','statususer');
INSERT INTO "django_content_type" VALUES(17,'kpp','videoclient','kpp');
INSERT INTO "django_content_type" VALUES(18,'document','videoclient','document');
INSERT INTO "django_content_type" VALUES(19,'category','videoclient','category');
INSERT INTO "django_content_type" VALUES(20,'user','videoclient','user');
INSERT INTO "django_content_type" VALUES(21,'login journal','videoclient','loginjournal');
INSERT INTO "django_content_type" VALUES(22,'group person','videoclient','groupperson');
INSERT INTO "django_content_type" VALUES(23,'person','videoclient','person');
INSERT INTO "django_content_type" VALUES(24,'person id','videoclient','personid');
INSERT INTO "django_content_type" VALUES(25,'Роль','videoclient','rule');
INSERT INTO "django_content_type" VALUES(26,'rule group','videoclient','rulegroup');
INSERT INTO "django_content_type" VALUES(27,'camera','videoclient','camera');
INSERT INTO "django_content_type" VALUES(28,'journal','videoclient','journal');
INSERT INTO "django_content_type" VALUES(29,'default params','videoclient','defaultparams');
INSERT INTO "django_content_type" VALUES(30,'ground','videoclient','ground');
INSERT INTO "django_content_type" VALUES(31,'visiting card','videoclient','visitingcard');
INSERT INTO "django_content_type" VALUES(32,'positions status','videoclient','positionsstatus');
CREATE TABLE "django_session" (
    "session_key" varchar(40) NOT NULL PRIMARY KEY,
    "session_data" text NOT NULL,
    "expire_date" datetime NOT NULL
);
INSERT INTO "django_session" VALUES('b82baa181f742b6478d4245853a9eafa','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-10-29 13:11:54.377809');
INSERT INTO "django_session" VALUES('6b5a96ed975193594d7c9e9fc738f4ea','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-10-29 13:12:19.122177');
INSERT INTO "django_session" VALUES('8cb831840824be61e87b7a1a71d902e5','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-10-29 13:12:44.028980');
INSERT INTO "django_session" VALUES('142e6d282f5f641942e63ba720a1eaaf','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-10-29 13:12:48.319073');
INSERT INTO "django_session" VALUES('24bf74fec7e1afd3fec322cc76e76224','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-10-29 13:16:22.206643');
INSERT INTO "django_session" VALUES('a25bb456bfb08b22ea4f606f684fd776','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-10-29 13:44:05.194422');
INSERT INTO "django_session" VALUES('39677fccb6a718cd0c690d08715a93f8','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-10-31 09:41:08.759360');
INSERT INTO "django_session" VALUES('b09bf261c40ec30ca3ef308ef2952d54','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-10-31 15:54:05.958514');
INSERT INTO "django_session" VALUES('eba3f78e00911446e03272d798cef5b8','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-10-31 17:12:12.575723');
INSERT INTO "django_session" VALUES('afef4227435a15d697bbb88608d692d7','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-01 11:34:51.352745');
INSERT INTO "django_session" VALUES('c54dcababffd281ac8811aaaeb265411','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-01 16:00:00.413941');
INSERT INTO "django_session" VALUES('12e1414c067e022609d3782d3e6cdc27','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-02 14:16:31.523333');
INSERT INTO "django_session" VALUES('898b3f0eb4a42e3dead543109ad65edb','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-03 08:28:29.472846');
INSERT INTO "django_session" VALUES('ce4d890ca9c1184a20bf80f750e7aed5','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-03 08:28:58.917658');
INSERT INTO "django_session" VALUES('38861b485a782984f597444d85de775c','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-03 08:29:16.019666');
INSERT INTO "django_session" VALUES('334fe3a2be412ab88be086b3793d1d86','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-03 12:21:04.606883');
INSERT INTO "django_session" VALUES('eccaa25013b00f6d79ce6779f0c94f45','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-03 12:26:35.468335');
INSERT INTO "django_session" VALUES('438e92baf5e62ce27a7b7206f23544d8','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-03 13:02:09.348051');
INSERT INTO "django_session" VALUES('4a5e23513bddad031f8378d29df88291','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-04 11:33:31.232246');
INSERT INTO "django_session" VALUES('7bfa6cfa0b1a9165a35b69ad75d5bfd1','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-04 12:30:23.118750');
INSERT INTO "django_session" VALUES('d182a8b118a671ba12e9b11e977c1b23','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-04 17:22:42.066234');
INSERT INTO "django_session" VALUES('08666fa5bd0044bcc71b6ab648c4617b','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-05 07:27:11.570926');
INSERT INTO "django_session" VALUES('f955df667e2c4db7ad921edd6dfca1ac','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-06 12:03:28.122498');
INSERT INTO "django_session" VALUES('6a31e0b67fb33e3d74dbc6de995aa7f3','gAJ9cQFVCnRlc3Rjb29raWVxAlUGd29ya2VkcQNzLmU5MGU4ZTRiZjNmMDUxMzhiYzZiYWMyZWRl
MGE0Nzg1
','2010-11-06 14:24:50.970545');
INSERT INTO "django_session" VALUES('00c045a412d957afbb378b24afcc0088','gAJ9cQEoVQp0ZXN0Y29va2llcQJVBndvcmtlZHEDVRJfYXV0aF91c2VyX2JhY2tlbmRxBFUpZGph
bmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmRxBVUNX2F1dGhfdXNlcl9pZHEG
SwF1LjEzNWRlODZhNzM0ODAxOWM1Y2Y2ZGMxMDdmNzY4MTFh
','2010-11-06 14:26:08.592830');
INSERT INTO "django_session" VALUES('b78d614c2c687bc03efbc09b5f63b453','gAJ9cQEoVQp0ZXN0Y29va2llcQJVBndvcmtlZHEDVRJfYXV0aF91c2VyX2JhY2tlbmRxBFUpZGph
bmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmRxBVUNX2F1dGhfdXNlcl9pZHEG
SwF1LjEzNWRlODZhNzM0ODAxOWM1Y2Y2ZGMxMDdmNzY4MTFh
','2010-11-06 14:34:50.171928');
INSERT INTO "django_session" VALUES('d0905d29d7343c7c37eb266f8652f617','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-06 15:38:14.332499');
INSERT INTO "django_session" VALUES('cfbf91c50896ce08e07b0edd1bae020c','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-06 15:38:15.591132');
INSERT INTO "django_session" VALUES('0a7b32d06b00fffb903c92e3b3d4163b','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-06 20:12:42.615853');
INSERT INTO "django_session" VALUES('8113582a60b45127fb4cb493b80e150e','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-06 20:40:09.436953');
INSERT INTO "django_session" VALUES('d5f95e7c6cf30c30a005cdba4f959cd1','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-06 21:50:04.774655');
INSERT INTO "django_session" VALUES('a5740d3be90ff680a25a3a7b554ae509','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-07 06:48:05.396765');
INSERT INTO "django_session" VALUES('674bf6eb80854335db074064360b8ce4','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-07 08:20:58.779739');
INSERT INTO "django_session" VALUES('147489696dbcef57555112ce1cfb28d2','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-08 06:05:59.187038');
INSERT INTO "django_session" VALUES('81dfcf82fdfae23c28447f682215cd38','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-09 16:57:50.954529');
INSERT INTO "django_session" VALUES('e74bbd7e3a93ed6a6f3a4e5b20facf2c','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-09 17:45:39.192415');
INSERT INTO "django_session" VALUES('0963bd0cfb5e785de3c94becb74e0002','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-10 06:52:56.364218');
INSERT INTO "django_session" VALUES('bcd3e31fd0dd2f411450d845ddadb8a3','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:12:10.795980');
INSERT INTO "django_session" VALUES('a92bf247e1e1b11c3d20ad31c565ccf0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:12:13.841901');
INSERT INTO "django_session" VALUES('ddfacc3bde57a922cdf5897b4e7b9dd8','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:12:16.886290');
INSERT INTO "django_session" VALUES('3f978cec433d261dce0912b83aa23b5a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:12:19.930480');
INSERT INTO "django_session" VALUES('a52cbdaf649f9c4ac14a7f8c92a03e00','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:12:22.979541');
INSERT INTO "django_session" VALUES('5c38e0207c8c9c695aadd17038f5608f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:12:26.022820');
INSERT INTO "django_session" VALUES('01928d2a72214812c69a1fd82ad3499c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:12:32.109059');
INSERT INTO "django_session" VALUES('49ad965a3958a704179917de6739cb9d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:12:35.271437');
INSERT INTO "django_session" VALUES('b2d252fa7bf66c9e8976b5d97bc0a49b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:12:38.373359');
INSERT INTO "django_session" VALUES('747db37455dcd47141cbf6f74bf91cb4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:12:41.498276');
INSERT INTO "django_session" VALUES('8ec91f2a66ddae7a5b0379588f3fb6c3','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:12:44.607794');
INSERT INTO "django_session" VALUES('2d3beee54cd8f693c0730e5db6c07c19','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:12:47.727264');
INSERT INTO "django_session" VALUES('6434be0f63dce8a9d9a8003fe1e3c5a0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:12:50.829188');
INSERT INTO "django_session" VALUES('f748e1e0798531afadba3b0fd5e0b95a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:12:53.996481');
INSERT INTO "django_session" VALUES('7119910202e322721be27316b77670d2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:12:57.082038');
INSERT INTO "django_session" VALUES('38596a565fcfd7bd550802eb55b99c7f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:00.163046');
INSERT INTO "django_session" VALUES('638da84a33dcfbc2575d62faafe9a405','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:03.292972');
INSERT INTO "django_session" VALUES('26a6ad34b808e60cdc1f02513baa6a34','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:06.325248');
INSERT INTO "django_session" VALUES('c52b9f689c4605d9df58b998f44f4e9a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:09.372646');
INSERT INTO "django_session" VALUES('3c4cd5563443c4b8f8adf88acbae3ad4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:12.421130');
INSERT INTO "django_session" VALUES('0567c15841c4ce81d0536420d65f194b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:15.464563');
INSERT INTO "django_session" VALUES('a2775676c713d86c22b9ec8d56dad9ba','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:18.511621');
INSERT INTO "django_session" VALUES('201e232af513b507a1d319613ff55142','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:21.557457');
INSERT INTO "django_session" VALUES('67d8352e07df8ea393d5f84dd0b2b995','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:24.603169');
INSERT INTO "django_session" VALUES('ebed78ca4ff89f7381542faf9e138e66','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:27.647980');
INSERT INTO "django_session" VALUES('3e2b53abacf1c95b65a53b9a1d49b3ea','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:30.749619');
INSERT INTO "django_session" VALUES('871b5324fa893c2e4a7c790bd0c38e18','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:33.796979');
INSERT INTO "django_session" VALUES('609699e558f758e74daf2ad370d3769c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:36.844093');
INSERT INTO "django_session" VALUES('96efd2f3a82d6e471ab3b0589e297c98','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:39.889613');
INSERT INTO "django_session" VALUES('b1d039e114add833487f9f0cc3e4ac17','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:42.935090');
INSERT INTO "django_session" VALUES('89c765e26af72d8ed8a3df8e9e884c80','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:45.985373');
INSERT INTO "django_session" VALUES('221c114a391bc8a2083b79402a40b839','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:49.031710');
INSERT INTO "django_session" VALUES('2037840f7383c0998907fe1b21d147fe','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:52.078392');
INSERT INTO "django_session" VALUES('af6f60cc544b464c33ec20d19c538e6b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:55.122919');
INSERT INTO "django_session" VALUES('2c515dc46cb62a41d9274b93b33789c4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:13:58.173632');
INSERT INTO "django_session" VALUES('ea0ffbcf0b53f54d43ad50d95136b54c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:01.217663');
INSERT INTO "django_session" VALUES('c1832d3ed38148be30efe21a77370f6c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:04.317533');
INSERT INTO "django_session" VALUES('1d2c0bdb254ae675ec8d25a41f12a1de','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:07.363519');
INSERT INTO "django_session" VALUES('7d9ca6accc116eee8525538f01d40a74','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:10.410619');
INSERT INTO "django_session" VALUES('f61e8af7bb172105843854e57198439a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:13.463855');
INSERT INTO "django_session" VALUES('6ed2ae0913b2a4e93c48953b07ec240a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:16.507084');
INSERT INTO "django_session" VALUES('f93fa82648a66fc7f45e0c51d9250089','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:19.553287');
INSERT INTO "django_session" VALUES('7ba1936561743a60e6c31fc204ee02a8','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:22.597695');
INSERT INTO "django_session" VALUES('16713164cdf1880bec25c1f49b99b604','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:25.660045');
INSERT INTO "django_session" VALUES('ec6ff73fcd999fbbcbe0eaaae2e67352','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:28.703835');
INSERT INTO "django_session" VALUES('6362b5c871a142273ea85015a4e199ed','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:31.748006');
INSERT INTO "django_session" VALUES('5b532be85575a3c2d78d24946ffee22b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:34.789456');
INSERT INTO "django_session" VALUES('879c749281444b7cfb84d508c205b01f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:37.843672');
INSERT INTO "django_session" VALUES('7e4e749b2f602753c9ae439671c65d16','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:40.889297');
INSERT INTO "django_session" VALUES('5680804dc90154e1d1ab614258ed586a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:43.942559');
INSERT INTO "django_session" VALUES('03c81d8727670716bb10978275ca1e53','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:46.971310');
INSERT INTO "django_session" VALUES('b84676734f82a5f27ab55246abb98608','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:50.016919');
INSERT INTO "django_session" VALUES('1201260c72c7dd2236fadb97ffa61220','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:53.131517');
INSERT INTO "django_session" VALUES('a6cbed9a4c46d7caf3be2f549f42e937','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:56.176767');
INSERT INTO "django_session" VALUES('a70fe8b23bac1109fde50ca319c88a52','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:14:59.223953');
INSERT INTO "django_session" VALUES('e690dcbe48f8c6fa1fe5df3fb5bd672a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:02.282751');
INSERT INTO "django_session" VALUES('200a7640bf298db652454cff61b5dcdf','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:05.326183');
INSERT INTO "django_session" VALUES('2f842084c64abaa349ae58765bd22de9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:08.372349');
INSERT INTO "django_session" VALUES('0161e3b13de35233f085dab4fdfa170d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:11.444109');
INSERT INTO "django_session" VALUES('e9842c9b44d585ef5f3b240766d1de58','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:14.490847');
INSERT INTO "django_session" VALUES('3ec1b871149492397f074cfde21a2e59','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:17.536636');
INSERT INTO "django_session" VALUES('e205566455087704f97a161b1782dd6f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:20.579509');
INSERT INTO "django_session" VALUES('fedf3b6739abeda022e754d0acf7ec80','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:23.629091');
INSERT INTO "django_session" VALUES('7e60f2bead2d6a6ac35edf98cb3f594e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:26.713555');
INSERT INTO "django_session" VALUES('8fc78da214976c8ce90de78db8711308','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:29.756994');
INSERT INTO "django_session" VALUES('a146ba2f32cb41fc03ff2ad26df2fdc2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:32.804559');
INSERT INTO "django_session" VALUES('576001f10f4ae2edfd28afb9d01c05e0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:35.855265');
INSERT INTO "django_session" VALUES('8b956a239e42dd6de48d8115e4199c2a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:38.898877');
INSERT INTO "django_session" VALUES('aa47d47ddcddd03fb963181b6e26051b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:41.972354');
INSERT INTO "django_session" VALUES('c49e20ea910a9ca23264f7a1eca95300','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:45.018587');
INSERT INTO "django_session" VALUES('f973a4a662378d11f1ac0fd013ec293a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:48.065915');
INSERT INTO "django_session" VALUES('119a2b4e2229e564aa52cccf55c48626','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:51.113218');
INSERT INTO "django_session" VALUES('6eb6cb25ec382e2848be76d0e8e2a49f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:54.155429');
INSERT INTO "django_session" VALUES('e2df0f413cafab21b7ffbafa7fe23af5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:15:57.200260');
INSERT INTO "django_session" VALUES('be79fdbbea3441a4402a7b7cef45e6b1','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:00.251513');
INSERT INTO "django_session" VALUES('6026f5941e933691495492a462a3937d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:03.297342');
INSERT INTO "django_session" VALUES('9f5de4e19a7b78d12d65af5569e40105','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:06.345772');
INSERT INTO "django_session" VALUES('5da04490414c2820dd0ef1c7ac5e5e55','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:09.386169');
INSERT INTO "django_session" VALUES('17d8568203c4f8ee570a82794c6366e2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:12.431686');
INSERT INTO "django_session" VALUES('9c25b2bdb644b3cb64edfe9b9aba0e4f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:15.474289');
INSERT INTO "django_session" VALUES('af81016a1f7695dc881aa0df6ed9cb89','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:18.526770');
INSERT INTO "django_session" VALUES('54ae58c893a6d7bd2aba3629b781423d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:21.568618');
INSERT INTO "django_session" VALUES('7256df783fe1689c581c685e0f30c735','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:24.613451');
INSERT INTO "django_session" VALUES('090935247c2cdcdaea537785b8b614b0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:27.703781');
INSERT INTO "django_session" VALUES('026fd099bcc0b6cc5de881ee8c2c4723','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:30.839956');
INSERT INTO "django_session" VALUES('fd9fc60fea8c064f0b5fbf2fb9b7dd06','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:33.895953');
INSERT INTO "django_session" VALUES('ce480a7095aca95b1a311597e615d66c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:36.927412');
INSERT INTO "django_session" VALUES('ae9a391457c84f6669cea40aadbc5954','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:39.972255');
INSERT INTO "django_session" VALUES('d6ff070297ea4bc95cdef267bd17bc1f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:43.002336');
INSERT INTO "django_session" VALUES('db019aaf2ffeac0a7cdb3ab85bac6d8c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:46.080215');
INSERT INTO "django_session" VALUES('472c5149e098d66fb08883471a6a84d4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:49.123980');
INSERT INTO "django_session" VALUES('4bcb52b3963085ba8eca3b3dac52fb31','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:52.171857');
INSERT INTO "django_session" VALUES('254c2d043ec850fe108339c4328c9aef','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:55.218727');
INSERT INTO "django_session" VALUES('8035a60879038c007ebd2b6471b7b02a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:16:58.265474');
INSERT INTO "django_session" VALUES('7d9703bac4a2072b11090328fdec5c2f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:01.761018');
INSERT INTO "django_session" VALUES('3863eb414b55240c37ed49c415ae5da9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:06.630027');
INSERT INTO "django_session" VALUES('9d16b1aabfd31f425df8b2775f3486c6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:09.673494');
INSERT INTO "django_session" VALUES('2df0e019dd1945dc105ef13caec236ca','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:12.720653');
INSERT INTO "django_session" VALUES('df035de4c3a4c05d4c80e5e2772e7c41','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:15.779740');
INSERT INTO "django_session" VALUES('f40c21808768ec9fb67c98142739531d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:18.823998');
INSERT INTO "django_session" VALUES('5e89b58007d87f312174cd3534147721','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:21.883447');
INSERT INTO "django_session" VALUES('5af5b3d92a036e260fae8238fc94c01e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:24.927700');
INSERT INTO "django_session" VALUES('73e7055deefa34e0609b249da1676a95','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:28.014612');
INSERT INTO "django_session" VALUES('113653be5f4ffd2f68ff6b466ed7823a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:31.061846');
INSERT INTO "django_session" VALUES('8c24a9957c69031046889eb53f2fb4bd','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:34.124241');
INSERT INTO "django_session" VALUES('aab74193deb332e73f9a790f8b47fd74','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:37.171155');
INSERT INTO "django_session" VALUES('be7985c7adbf7082fc631b20ec45d1ff','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:40.205095');
INSERT INTO "django_session" VALUES('a2af03b48cd6ca197be7fdb9b9560358','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:43.252973');
INSERT INTO "django_session" VALUES('f54259cb1cb57bb9f360e861e9a0db15','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:46.289040');
INSERT INTO "django_session" VALUES('fb12e3043137fd0d036b0984f9d9762d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:49.358434');
INSERT INTO "django_session" VALUES('d808c387fd57b2651a09b8de62f1480e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:52.409600');
INSERT INTO "django_session" VALUES('b1c56659ed9bf912ee1d6a6536f19748','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:55.455210');
INSERT INTO "django_session" VALUES('8d12df519cb765ee2b64b33dfc79e3f0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:17:58.508618');
INSERT INTO "django_session" VALUES('84444b7cdbeabb632e367c1ad970cc9c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:01.587898');
INSERT INTO "django_session" VALUES('5b8d7b63ad71fa4b1c0df5855b3bdf72','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:04.629638');
INSERT INTO "django_session" VALUES('6a2a9bcdcf4a9cf07d12ba58bba552a8','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:07.716894');
INSERT INTO "django_session" VALUES('aa188ce2cc24c323d43a43f93796ff4f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:10.766499');
INSERT INTO "django_session" VALUES('8a63db0647401f5cd0974a4d6f3c2e5d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:13.814749');
INSERT INTO "django_session" VALUES('4de6ec31a9f9b9b62dbe63b0b4398aaf','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:16.860253');
INSERT INTO "django_session" VALUES('dc9b63acf6f80856b03e6323353b296a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:19.906183');
INSERT INTO "django_session" VALUES('44ad7da9f67ef892a8512326ef2b9555','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:22.951707');
INSERT INTO "django_session" VALUES('50e3d19b195066aaf15f7dc39614e0ad','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:25.999487');
INSERT INTO "django_session" VALUES('2aea95a6edf1afc57b73242ba736b378','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:29.050287');
INSERT INTO "django_session" VALUES('de87493d473b814716e000d0a39ca6fc','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:32.102932');
INSERT INTO "django_session" VALUES('9769664597b5dbf541d852a2e395442a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:35.147452');
INSERT INTO "django_session" VALUES('d15c6cb4502800f6d72c5fca57aebbb9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:38.178825');
INSERT INTO "django_session" VALUES('f2049463337130c4506cd6cd4cb22cdc','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:41.301369');
INSERT INTO "django_session" VALUES('9698f756fe0d3a100fba7305bbcf7422','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:44.354188');
INSERT INTO "django_session" VALUES('89a4264789823b1542db116f37705bde','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:47.401843');
INSERT INTO "django_session" VALUES('729f140ca12dc87462b76ba343fdedf7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:50.444615');
INSERT INTO "django_session" VALUES('63804594c85165af336314664dfef97a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:53.489475');
INSERT INTO "django_session" VALUES('99f34503277c53bee62231a8f251208c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:56.539452');
INSERT INTO "django_session" VALUES('0e67399c4cb11287404efc81bcdcf3cd','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:18:59.580569');
INSERT INTO "django_session" VALUES('50f5f7041beee3aaccf90bad16f09426','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:02.628934');
INSERT INTO "django_session" VALUES('b5d0effc8e5b4da20c5677600015bc3c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:05.688706');
INSERT INTO "django_session" VALUES('9bc24855bbb1051fad70fef0443ef098','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:08.731269');
INSERT INTO "django_session" VALUES('d3eda3e5b4b4a7f195ce566af0fdbb61','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:11.795827');
INSERT INTO "django_session" VALUES('44c9d791255c059932436001ef5da5a0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:14.839829');
INSERT INTO "django_session" VALUES('d56fce7aea7991a444f2956f43f3d4f2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:18.224110');
INSERT INTO "django_session" VALUES('91f36e16338ce65ac464a0ade1a133da','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:21.362659');
INSERT INTO "django_session" VALUES('6ae20d303cc148a8827c11a68897b79a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:24.767472');
INSERT INTO "django_session" VALUES('86a921495b12fc88d99c94c24ccf19ee','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:27.817258');
INSERT INTO "django_session" VALUES('a68e6849f6e9a9e41226addf82dd0944','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:30.862668');
INSERT INTO "django_session" VALUES('25c1f30b2ba38666d253765977733eb4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:33.909648');
INSERT INTO "django_session" VALUES('8ad0b1d8848b2ae42b9898bbba364262','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:37.705033');
INSERT INTO "django_session" VALUES('7068fa6c90de605ad2be5f47aaeb46cf','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:40.796088');
INSERT INTO "django_session" VALUES('9e0ecf180c94ec8318488ea6ef4c8879','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:43.828387');
INSERT INTO "django_session" VALUES('9becde0e1c182d459696cab2f52bb2e7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:46.876135');
INSERT INTO "django_session" VALUES('ddd4bd2db13d2a46f37e3d2ce4b095ba','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:49.910310');
INSERT INTO "django_session" VALUES('57b87875fd5a26d97f65cdb135b41831','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:52.952455');
INSERT INTO "django_session" VALUES('6850444ab9dcb5195e156921cea7323c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:55.997013');
INSERT INTO "django_session" VALUES('dedce40ce157715369b1965e3aa9bd26','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:19:59.041267');
INSERT INTO "django_session" VALUES('5fb1f18295172eef3fec42b7ad88cd46','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:02.087122');
INSERT INTO "django_session" VALUES('4917384ea829d3eb2a029190f363ac81','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:05.208068');
INSERT INTO "django_session" VALUES('f7baf11b6b2e24c7a2c2eaecaafd5f99','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:08.241522');
INSERT INTO "django_session" VALUES('d31f759b55c98ceb3f0ca3c3f2e45c70','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:11.289995');
INSERT INTO "django_session" VALUES('4e45860f7e5f551ce6c36c43930f4d76','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:14.327228');
INSERT INTO "django_session" VALUES('c5ae11ef970e90cd64509308a4fc6bfb','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:17.372583');
INSERT INTO "django_session" VALUES('b9df92bb380828a233e19924451d9ff0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:20.433326');
INSERT INTO "django_session" VALUES('de91726c70afa9531a83208b7c95756b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:23.522686');
INSERT INTO "django_session" VALUES('4906147cba6cb4d2b11bff29f4c382a1','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:26.569163');
INSERT INTO "django_session" VALUES('a084bf9d275ea055ab0a30e5961487e0','gAJ9cQEoVQ1fYXV0aF91c2VyX2lkcQJLAVUSX2F1dGhfdXNlcl9iYWNrZW5kcQNVKWRqYW5nby5j
b250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kcQRVE2xhc3Rfam91cm5hbF91cGRhdGVx
BWNkYXRldGltZQpkYXRldGltZQpxBlUKB9oLDRMeFADbSIVScQd1LjIyNDVkZDRkNjc0ZTNkZjE2
Y2E1MzliOWRkZTRlYWU5
','2010-11-27 19:30:20.056387');
INSERT INTO "django_session" VALUES('a3a15d17cebf93ed4b77c30879fe547c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:29.627384');
INSERT INTO "django_session" VALUES('060aa751a234ab17131b86b2b99a94a7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:32.681340');
INSERT INTO "django_session" VALUES('010971d08ce282e494e095cb3daabb22','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:36.747441');
INSERT INTO "django_session" VALUES('fec4888df6b5579739140490f27b93ef','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:39.850582');
INSERT INTO "django_session" VALUES('ccdaec4fe40d9f754bd7659cde891087','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:42.897314');
INSERT INTO "django_session" VALUES('87e0ac6700f1b69e77957fd24728399f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:45.956396');
INSERT INTO "django_session" VALUES('68686cea86730901b92038eb16004a37','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:49.007964');
INSERT INTO "django_session" VALUES('0bc7b10c320afe656f92ff346284254a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:52.042850');
INSERT INTO "django_session" VALUES('a8b4846c063507f7fdf894d54bb27e56','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:55.090840');
INSERT INTO "django_session" VALUES('71d7d7f4e0f4aa9396bdebf9782568b3','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:20:58.139291');
INSERT INTO "django_session" VALUES('1af1103ad191a79f4f32c4f503ef2aad','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:01.182666');
INSERT INTO "django_session" VALUES('ab1c3ee51b09ae925c3ddf7b8b2ec2b2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:04.239872');
INSERT INTO "django_session" VALUES('a48f8e8c41e942c06d3af9e57a999498','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:07.285404');
INSERT INTO "django_session" VALUES('b9a9bb8c575acf938e1ee3662315f49c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:10.328049');
INSERT INTO "django_session" VALUES('9d5951370e01bf110d074815e7934647','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:13.370826');
INSERT INTO "django_session" VALUES('b5fd413a1cfd2ca49580905c85f38ba5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:16.419492');
INSERT INTO "django_session" VALUES('1cc1f3abd11b77bba12138a3ad7b5234','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:19.463772');
INSERT INTO "django_session" VALUES('d6c92a82169826e0a087ee57a7f3c059','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:22.510210');
INSERT INTO "django_session" VALUES('80b288a5074c20410ebec2974fdfaa8e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:25.555509');
INSERT INTO "django_session" VALUES('94945bbdc0463ac4eb96d01109f5c4b6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:28.600418');
INSERT INTO "django_session" VALUES('09316372d62ec199e74ded5fed0a2da7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:31.631610');
INSERT INTO "django_session" VALUES('e58b25a0ccb5a0eb2a18d408fdd163ff','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:34.666287');
INSERT INTO "django_session" VALUES('d7d97725e72ff1350d47c39028887b4a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:37.713106');
INSERT INTO "django_session" VALUES('da0ad02ef4fb7db57fec62a50f45f016','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:40.773149');
INSERT INTO "django_session" VALUES('ca33ae94cd4b6edfe749f6322de0429b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:43.820392');
INSERT INTO "django_session" VALUES('21a39e10b4c129b7288df6a0d25f2de3','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:46.861922');
INSERT INTO "django_session" VALUES('a922648d00681aa9c5d98e755769304f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:49.904579');
INSERT INTO "django_session" VALUES('afc7881b502a9c4b6e3ed82d0210f943','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:52.948071');
INSERT INTO "django_session" VALUES('6a5b6d754c6761d304465fb5be855808','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:55.993454');
INSERT INTO "django_session" VALUES('ad14bf7b3f0490ab20ace668aa08572b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:21:59.036949');
INSERT INTO "django_session" VALUES('d3179acc1637428a798021e84d305a14','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:02.082481');
INSERT INTO "django_session" VALUES('06030a7bebb3005416bbd567eb0faa72','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:05.130642');
INSERT INTO "django_session" VALUES('5b8fd49d36c791252bd05c250ecd82cd','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:08.173883');
INSERT INTO "django_session" VALUES('a5a8f8863a5f75bb54ab8972b4b3fc9e','gAJ9cQEoVRh3YWl0X3VuaWRlbnRpZmllZF9wZXJzb25xAolVEl9hdXRoX3VzZXJfYmFja2VuZHED
VSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEEVQ1fYXV0aF91c2Vy
X2lkcQVLAVUTbGFzdF9qb3VybmFsX3VwZGF0ZXEGY2RhdGV0aW1lCmRhdGV0aW1lCnEHVQoH2gsP
EyU7BQm8hVJxCHUuYzFmMzZmM2RjZWJiZDIxZDc2NTlhODJiNDkyNGQ1NmI=
','2010-11-29 19:38:33.426728');
INSERT INTO "django_session" VALUES('52837a158f15da4edd99e593bcb82fa0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:11.237393');
INSERT INTO "django_session" VALUES('aa43f152710674787e7e944cb2dcf72c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:14.279615');
INSERT INTO "django_session" VALUES('54fa1b8c67a0fed52af75dfde2999c83','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:17.325427');
INSERT INTO "django_session" VALUES('dcf705af0012fa22221496e26f3a972f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:20.369940');
INSERT INTO "django_session" VALUES('fd497672b2497b9f6eec9d76dc6a2f2f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:23.415591');
INSERT INTO "django_session" VALUES('6b5531937bae070611e4ed5e054ee93c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:26.467876');
INSERT INTO "django_session" VALUES('ac852c877454a7670c17951f7c9c0222','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:29.511164');
INSERT INTO "django_session" VALUES('ece66c658d5a4abc9b36897f2857f610','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:32.554075');
INSERT INTO "django_session" VALUES('157dfb2f454ff26edba9d1129dce9886','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:35.603517');
INSERT INTO "django_session" VALUES('74b85e5f3e0e26997470484849c789ab','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:38.645381');
INSERT INTO "django_session" VALUES('f75f017ad98b3cce333bcffbf05384e6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:41.725630');
INSERT INTO "django_session" VALUES('a8d39b32ad8afc1a6c7a707d810bb446','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:44.767614');
INSERT INTO "django_session" VALUES('97faa9c00d078655accfaf8986f16e59','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:47.827811');
INSERT INTO "django_session" VALUES('c3d56c67074e28576f713ef615875a62','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:50.951085');
INSERT INTO "django_session" VALUES('02ccdecc6b42289dd43c244d9525005f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:53.990012');
INSERT INTO "django_session" VALUES('79e747681a30821432c9a271c0ac1d07','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:22:57.049274');
INSERT INTO "django_session" VALUES('8917dd10349a3838b5be96d1c431db81','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:00.095172');
INSERT INTO "django_session" VALUES('21626fddcc0fe7e5c8aa41ddf1b02c70','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:03.214181');
INSERT INTO "django_session" VALUES('3bd694e9645dcdfd68aef150b1287273','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:07.283804');
INSERT INTO "django_session" VALUES('8b142385a46742fdfe0f3d1404b3e844','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:10.389765');
INSERT INTO "django_session" VALUES('bd178682b101db003421c187af029054','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:13.748731');
INSERT INTO "django_session" VALUES('cbb0dde8e3806ffdd99650c0a08cb579','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:16.831516');
INSERT INTO "django_session" VALUES('d9bdc976192dc2360c39731ace7d2cd0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:22.557814');
INSERT INTO "django_session" VALUES('732de4022c55fc43065db66ea6b04238','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:25.690408');
INSERT INTO "django_session" VALUES('7a14fe0570dadcc934b72187fa17a39e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:28.736401');
INSERT INTO "django_session" VALUES('a5b2d6825e5c32a833401c853798c2ad','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:31.768772');
INSERT INTO "django_session" VALUES('5bb1d64df266e560510bbb77028d486a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:34.815859');
INSERT INTO "django_session" VALUES('d4c82dc4d5c39e5c736c5bde86b09b53','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:37.859926');
INSERT INTO "django_session" VALUES('aec8d73f6a194716899740f2879d17a0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:40.903252');
INSERT INTO "django_session" VALUES('e5d5e13ea419f10c76189e2a4b181e03','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:43.948067');
INSERT INTO "django_session" VALUES('71d8bc9ab018f49b15668bf8a44a7a69','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:47.523847');
INSERT INTO "django_session" VALUES('73269bebb7c8afd0038056acbe699ae0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:50.566947');
INSERT INTO "django_session" VALUES('72b0ca1e2e56a40b295d219585e79f33','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:53.629760');
INSERT INTO "django_session" VALUES('9b49012fb66049a07316c7f8be3c502e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:56.679974');
INSERT INTO "django_session" VALUES('1b9672e08ffc4ad5aee150b0a0e6027f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:23:59.724142');
INSERT INTO "django_session" VALUES('25b90deff112564abee73719539095b3','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:02.766564');
INSERT INTO "django_session" VALUES('45d404c4ea4488afae440af06a1113cc','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:05.819533');
INSERT INTO "django_session" VALUES('5a13b70c9bc690c48d3743a64f68862d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:08.877581');
INSERT INTO "django_session" VALUES('f8697949b718a60a0b71a35330d4a463','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:11.921011');
INSERT INTO "django_session" VALUES('2746a47939cc8e90a90e75c335445caa','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:14.968419');
INSERT INTO "django_session" VALUES('e2234fd5ad72aca354521b05201038b4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:18.016266');
INSERT INTO "django_session" VALUES('c0b92d8b25bfa39ae526755f813f2166','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:21.118554');
INSERT INTO "django_session" VALUES('784d867aa270cc1d77d9697224e3ea91','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:24.163327');
INSERT INTO "django_session" VALUES('8ef2823c94eee2b952a3f6d676ade1d8','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:27.208177');
INSERT INTO "django_session" VALUES('1cca6d48fefb5248bbc8f97a4df08e0e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:30.238543');
INSERT INTO "django_session" VALUES('607993ccd639b4890ca2af8be73dda9c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:33.285508');
INSERT INTO "django_session" VALUES('ef9d6ca47cdbbafb6093a6d9742c31e5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:36.376532');
INSERT INTO "django_session" VALUES('a4afd5d1ceebf1bcaac825795bc8e3cd','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:39.425745');
INSERT INTO "django_session" VALUES('8013bf22bf212f88336c4868b4749399','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:42.472016');
INSERT INTO "django_session" VALUES('a4462c6b0606b08f9932d19e11629bd3','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:45.525601');
INSERT INTO "django_session" VALUES('57b8fa3aa2195dc15fbf5fd70d54f0c9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:48.577904');
INSERT INTO "django_session" VALUES('883e84b0f7d7580ca1a7471080fdd442','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:51.611815');
INSERT INTO "django_session" VALUES('39530df2d5dfd7d1049ab186eaa81e60','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:54.655745');
INSERT INTO "django_session" VALUES('a70cb16099d3f7ea55d694fe85bbb206','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:24:57.722189');
INSERT INTO "django_session" VALUES('99b797bac95b7fdfcac37b5f839d82a6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:00.764410');
INSERT INTO "django_session" VALUES('1b4d3d4e0093e7f8b218831a43f0baa5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:03.811256');
INSERT INTO "django_session" VALUES('af31154b1490970372690ef89eb62589','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:06.866782');
INSERT INTO "django_session" VALUES('556b9c48b6ae9a29ce8dffc43e2c06cc','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:09.913378');
INSERT INTO "django_session" VALUES('628dba22bfe6c13dae6e412ade0a3b69','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:12.960004');
INSERT INTO "django_session" VALUES('b99e8d78357f31cbb263675b9a4fb52a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:16.003088');
INSERT INTO "django_session" VALUES('11d2d225c05acac9e2b6c1df50999e51','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:19.048563');
INSERT INTO "django_session" VALUES('f9f632d6170c56461256d1d8858b2cdf','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:22.092961');
INSERT INTO "django_session" VALUES('ec5cf2b7460ef13890fd69d0a1154beb','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:25.136837');
INSERT INTO "django_session" VALUES('c2fe267d22e94c132089bfed78d3cd6a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:28.172392');
INSERT INTO "django_session" VALUES('43bc32175bc7469c2204e2c26b161dd6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:31.218832');
INSERT INTO "django_session" VALUES('77c332de25d31476e85ba5d16582d2a1','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:34.263631');
INSERT INTO "django_session" VALUES('f3e3bfc439128b3b99207bfbd0cbba5a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:37.324371');
INSERT INTO "django_session" VALUES('7c01d98cdd72ad0eb2ba008610b48c70','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:40.366122');
INSERT INTO "django_session" VALUES('bdae2f9050fa4c13f05ed3b6058ff00d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:43.413204');
INSERT INTO "django_session" VALUES('a1aa6645c3c772c08e28d03d01f2b4d4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:46.457814');
INSERT INTO "django_session" VALUES('5474717dd5c151e0dce445b757cca488','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:49.518364');
INSERT INTO "django_session" VALUES('fa0555e6f2df4e5822f1453fef17f5b3','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:52.566488');
INSERT INTO "django_session" VALUES('d545699d74b80188b8ca25fafb8c0f96','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:25:55.609673');
INSERT INTO "django_session" VALUES('b18fce16cfc33c8cb6d3f6b5912bc906','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:04.858965');
INSERT INTO "django_session" VALUES('3e3a9ee58df326bfb6ee59ad8f61284c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:07.899067');
INSERT INTO "django_session" VALUES('b1ee5dcd67f8a124e498f7a88605a7ca','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:10.943204');
INSERT INTO "django_session" VALUES('5b6d4cfc0b5dd07d2cd3f90f2803e078','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:13.988104');
INSERT INTO "django_session" VALUES('86a0f0919fde009396be1d41d6a356ca','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:17.034548');
INSERT INTO "django_session" VALUES('f6297ab392143b848f22dc9b87ad52f0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:20.078474');
INSERT INTO "django_session" VALUES('2c6ae9795d3d2b40a95a922133bd4a70','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:23.137376');
INSERT INTO "django_session" VALUES('53ce7740beef386e0b67a249a8d69917','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:26.184110');
INSERT INTO "django_session" VALUES('204ec9a1ffdba95459d1354dda044981','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:29.227481');
INSERT INTO "django_session" VALUES('9f44dd2bc995a5a62723350f70efbebd','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:32.272744');
INSERT INTO "django_session" VALUES('31742e9dfac7bbb01f8c9c93d13cada3','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:35.316315');
INSERT INTO "django_session" VALUES('cc3819d6fc18408bb26664b5c65b220b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:38.349647');
INSERT INTO "django_session" VALUES('6bd1fc9588620a77fef4e25b00a053ca','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:41.394759');
INSERT INTO "django_session" VALUES('2e9fd9973629ad92ad50ca69c3b0e6ac','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:44.430554');
INSERT INTO "django_session" VALUES('7f3cd11bfe99500cd3cda21499df203f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:47.473437');
INSERT INTO "django_session" VALUES('813d7a7ea37b5d5370b41284f089e75a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:50.519851');
INSERT INTO "django_session" VALUES('abfd6be2692a8229dd77865677af330a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:53.589931');
INSERT INTO "django_session" VALUES('8e437edf4cce147b98136911c52dd99c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:56.634322');
INSERT INTO "django_session" VALUES('ad5aebe64a625b1a569834dab8ae7969','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:26:59.694735');
INSERT INTO "django_session" VALUES('b903a1997f3f631f2783b45ca9688700','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:02.743162');
INSERT INTO "django_session" VALUES('42331d49b80cb352822ef831ac5d4018','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:05.785478');
INSERT INTO "django_session" VALUES('558ac879b52a71f8e337bc6c946fb9f4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:08.832107');
INSERT INTO "django_session" VALUES('eb78db76ecd323b50d950aff26e614c7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:11.878854');
INSERT INTO "django_session" VALUES('415af3acfa2215c3b04c5d90aa575439','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:14.921672');
INSERT INTO "django_session" VALUES('901e6a046fa65283c3ec99d16c01d851','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:17.968412');
INSERT INTO "django_session" VALUES('c626e9187a65e10ff87986241263d338','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:21.024960');
INSERT INTO "django_session" VALUES('c864811f5171b3e7ce6547900a83193e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:24.057385');
INSERT INTO "django_session" VALUES('4145b1c02e04064cda9c7712afeb7bf1','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:27.102563');
INSERT INTO "django_session" VALUES('eb58f7a0140e6a79547aae09d3bf12cd','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:30.150294');
INSERT INTO "django_session" VALUES('46e3d9e10f6e2d17d713a7558b7005f2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:33.190941');
INSERT INTO "django_session" VALUES('3aac7cd1447f1fc81ba0b07025f86cb5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:36.261271');
INSERT INTO "django_session" VALUES('6761913f863e17854e09c31c75ccad4b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:39.296985');
INSERT INTO "django_session" VALUES('9714458cc1077bc0451c19a8c5ebd1dd','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:42.345864');
INSERT INTO "django_session" VALUES('75e8025cf5c1d48ddc6025b5c3666c5e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:45.392660');
INSERT INTO "django_session" VALUES('3c3f99e57fb5ffba27185d8617ab66ad','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:48.465848');
INSERT INTO "django_session" VALUES('c60b87558a5e982a69ea9dd2a06afdcb','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:51.514025');
INSERT INTO "django_session" VALUES('1ba21bfe137fee583f70b16fe4004a17','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:54.560959');
INSERT INTO "django_session" VALUES('951bba0ed92f1621ec6784fad48d13be','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:27:57.637140');
INSERT INTO "django_session" VALUES('48fe88711beaa0d8c3e8eb4615b76807','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:00.682118');
INSERT INTO "django_session" VALUES('83a0e54bf268ed60b7d1b3c3c5413447','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:03.727033');
INSERT INTO "django_session" VALUES('cfd82815e7add7fbe782ff4b0e50559f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:07.747103');
INSERT INTO "django_session" VALUES('4085a0f574ad49cfaa2fd9271238930e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:10.872350');
INSERT INTO "django_session" VALUES('fc676d36440955f3d4a2d78bcec85b7d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:13.903804');
INSERT INTO "django_session" VALUES('d848a70bbfe97663f85d4f17388b2183','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:16.949339');
INSERT INTO "django_session" VALUES('70faa07b570085a95f351ac32e407f07','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:19.992512');
INSERT INTO "django_session" VALUES('07a62843f9a159e7537ddba5d1a47395','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:23.024369');
INSERT INTO "django_session" VALUES('8f2f6fd621c0b184d700742e2fc255ba','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:26.068195');
INSERT INTO "django_session" VALUES('f0bceecc7de8d921c81ac66152bc2e92','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:29.112830');
INSERT INTO "django_session" VALUES('ea497d4816855a380e6bf8c81c7e34b2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:32.158818');
INSERT INTO "django_session" VALUES('52bc01343319c9ec366fc750f576a093','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:35.204512');
INSERT INTO "django_session" VALUES('0255b3f333aa61b2f8bcaecef1bc7981','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:38.245757');
INSERT INTO "django_session" VALUES('92699353d50b07a26ee59f1f78c75b47','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:41.291200');
INSERT INTO "django_session" VALUES('46c103bcdc95ef36d6a2b15c0a0bd271','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:47.414803');
INSERT INTO "django_session" VALUES('ad0926d4e5b882e184f8a64e8932d22f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:52.027456');
INSERT INTO "django_session" VALUES('6dc822603ddacc6ccbff09de59f72e76','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:55.180866');
INSERT INTO "django_session" VALUES('58087db0dd0b1eb848c1b091d1975735','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:28:58.305634');
INSERT INTO "django_session" VALUES('4c2eeba0a2d86496990fb6b5cf98db64','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:01.355383');
INSERT INTO "django_session" VALUES('a6722888bb93fb525f8c57b41230e3d8','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:04.408865');
INSERT INTO "django_session" VALUES('492d65f33f21592081ef83dced6cc0a1','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:07.448515');
INSERT INTO "django_session" VALUES('ac22d94efe6679b048b31cceb0bac94a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:10.488731');
INSERT INTO "django_session" VALUES('52e9ce39159f9807e2611b6b930872d7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:13.540367');
INSERT INTO "django_session" VALUES('8cacaaeb20a51c914c7803f2c3a5317a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:16.580141');
INSERT INTO "django_session" VALUES('037fb91beee1af5234b59191ac61549f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:19.623747');
INSERT INTO "django_session" VALUES('7df04a61d87d6e0452932fac7179ae73','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:22.669575');
INSERT INTO "django_session" VALUES('abca166023cf39764e8ba3c93705a505','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:25.716854');
INSERT INTO "django_session" VALUES('c5202af705a274bd110c8187b7e5faa9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:28.762207');
INSERT INTO "django_session" VALUES('a7e120c6caf8b32981ba91f6397500f6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:31.815087');
INSERT INTO "django_session" VALUES('580352c041548a0b2f0995e16e0d8af7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:34.872953');
INSERT INTO "django_session" VALUES('e165b10651551c20b5008be9dd16922b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:37.912641');
INSERT INTO "django_session" VALUES('0cd058b5de23cf83c491a92d5b979c8b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:40.955797');
INSERT INTO "django_session" VALUES('e419e057130ce30b9474a841dbf477c9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:44.000010');
INSERT INTO "django_session" VALUES('ea522a3aee6e9dcc4685876cd95227ba','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:47.046014');
INSERT INTO "django_session" VALUES('8d26ecf429f20254c6ec01e5d6583279','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:50.093825');
INSERT INTO "django_session" VALUES('f8550afceebab7852e12c825ef9e740e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:53.141773');
INSERT INTO "django_session" VALUES('197a2bba696ea865d4bc3c3c1fd70bd2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:56.194711');
INSERT INTO "django_session" VALUES('4103888f73b14eb6cc8a533532353a89','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:29:59.299558');
INSERT INTO "django_session" VALUES('4fa0a82c56cd16809d096ded48389978','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:02.331052');
INSERT INTO "django_session" VALUES('9e474cf4df212e18f5d671f4c27684f4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:05.522584');
INSERT INTO "django_session" VALUES('70f62ae31b593e42d96ab81e9b1da1be','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:08.568625');
INSERT INTO "django_session" VALUES('011cdbad9459aeaf05717a874c455dea','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:11.615942');
INSERT INTO "django_session" VALUES('d47c79a21ffbe440af8b37c31bf66632','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:14.672079');
INSERT INTO "django_session" VALUES('f70cac976bc266cebdbeeaca3b99648b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:17.718044');
INSERT INTO "django_session" VALUES('ab3d08e6cd23fca0205c6e6f0301dd72','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:20.778095');
INSERT INTO "django_session" VALUES('e67677e2741cedc8f481f0df83db6800','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:23.824668');
INSERT INTO "django_session" VALUES('be634162e59ed698db22dfaf573386c0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:26.870413');
INSERT INTO "django_session" VALUES('2f25cd04dbf355f6729586a0a907989d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:29.928855');
INSERT INTO "django_session" VALUES('54af3e4670d136f372fbc6c37b54c10c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:32.974800');
INSERT INTO "django_session" VALUES('78ea4885eba07555ba444037b96d5932','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:36.087815');
INSERT INTO "django_session" VALUES('5d326ff46a3076ecf39a3f8f0777890e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:39.321446');
INSERT INTO "django_session" VALUES('19690ca10e8a293d5d0c754ce774ee0e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:42.371778');
INSERT INTO "django_session" VALUES('7b223b03dd7ac020e2731790e5d695ec','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:45.415974');
INSERT INTO "django_session" VALUES('c43327f4370a7e2c003201f49e6aafb3','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:48.460490');
INSERT INTO "django_session" VALUES('de814207800f8081168398ce31f132c0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:51.505818');
INSERT INTO "django_session" VALUES('25e4f53c887ceeaff4b8b9cb63b0f76d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:54.537276');
INSERT INTO "django_session" VALUES('89a92e7327c93629423ca630b976602f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:30:57.577053');
INSERT INTO "django_session" VALUES('637235869e5c95349f6c3ac4a43f8ec5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:00.621968');
INSERT INTO "django_session" VALUES('769834485ab2a74d64552bde56f42e79','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:03.663793');
INSERT INTO "django_session" VALUES('3d0c08ede65407453a1d070f93b46b31','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:06.710416');
INSERT INTO "django_session" VALUES('625c684667ea3aa3e33fc43dda8eb784','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:09.783148');
INSERT INTO "django_session" VALUES('75bfb74746c5f4ecf276cc8d082c1c06','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:12.827751');
INSERT INTO "django_session" VALUES('f85f7631aa8783cd9ac6e330b81dafb6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:15.871060');
INSERT INTO "django_session" VALUES('dabd8b73c9ae8a1527b1f2c7462d2701','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:18.914008');
INSERT INTO "django_session" VALUES('ce07f6488fe800359979607352ca0338','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:21.960622');
INSERT INTO "django_session" VALUES('6a2fa91fc9b34305eab3aff5b5e99f60','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:25.002971');
INSERT INTO "django_session" VALUES('4f159bc5a758c5d7f042ad847aaf3a70','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:28.047964');
INSERT INTO "django_session" VALUES('67523b0932b181f3c9a4e2e7655408ae','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:31.098956');
INSERT INTO "django_session" VALUES('a89a4344af223fb3031f10167bd466cc','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:34.152666');
INSERT INTO "django_session" VALUES('516c40b9e2fc419cdc58a08cc6639117','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:37.196061');
INSERT INTO "django_session" VALUES('ddbc8b8d12c19ce03dd0ab72eab856a5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:40.239060');
INSERT INTO "django_session" VALUES('23cfe6345413a89bfb3396073fdb9ae2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:43.284816');
INSERT INTO "django_session" VALUES('d0f86cf8707e8238cc49f31d852b5671','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:46.330299');
INSERT INTO "django_session" VALUES('1959cddf2c86acef22707a3227dd2559','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:49.374477');
INSERT INTO "django_session" VALUES('13e9cdf01da0258521e3fa895f1e7ab0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:52.422882');
INSERT INTO "django_session" VALUES('091d6ee25b13a90dadd4d0d72e4d4d63','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:55.463537');
INSERT INTO "django_session" VALUES('7a70167101a158629ea6ae18564c0a77','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:31:58.520139');
INSERT INTO "django_session" VALUES('fa38824dbdf7929b9922114964ca40d2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:01.567010');
INSERT INTO "django_session" VALUES('3c3a4ac3db4656bb19d627dfdd4281ce','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:04.611109');
INSERT INTO "django_session" VALUES('60b17d8965d5b9f5d67229bf11098dcf','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:07.659500');
INSERT INTO "django_session" VALUES('878ebbc94ea3be271d9269cf2145ef36','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:10.699402');
INSERT INTO "django_session" VALUES('e1f3c024607c18125bef448e8374329f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:13.745107');
INSERT INTO "django_session" VALUES('83baedc5d05b45c120f79dc2416d39f6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:16.871667');
INSERT INTO "django_session" VALUES('c976f2d025b048ac6e1ee2b2a72be56d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:19.908139');
INSERT INTO "django_session" VALUES('8b661d5a1f24ee76583ea5fe7ad6e4c2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:22.953293');
INSERT INTO "django_session" VALUES('b8c208acd1da08c8aecf722092c43de8','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:26.000461');
INSERT INTO "django_session" VALUES('5e992cbaa02fae738553b3b0f223237d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:29.176996');
INSERT INTO "django_session" VALUES('bcb0255ffa1baf561ddfc1c04ce3818a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:32.263979');
INSERT INTO "django_session" VALUES('8d77248110ccabaa167b2b78397668fc','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:35.309756');
INSERT INTO "django_session" VALUES('dfff5acb8885176b152a967caa208079','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:38.368094');
INSERT INTO "django_session" VALUES('34307e36ff8341356530e2ccb18f140d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:41.410594');
INSERT INTO "django_session" VALUES('ad9f4a55a22dfa584dca649821055b2b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:44.455254');
INSERT INTO "django_session" VALUES('03fb02af1abdebff2712a77d1a25a160','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:47.499462');
INSERT INTO "django_session" VALUES('e7827dbf89ce7beb1ab7f06844bd8a0d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:50.545546');
INSERT INTO "django_session" VALUES('e23fe5c505cac55c5a5b18ae7174c4cc','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:53.591038');
INSERT INTO "django_session" VALUES('13bfac12e6f0ac256f1bd076a0dc5688','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:56.646714');
INSERT INTO "django_session" VALUES('761fdb1d797f3426e2f4f7d9fc203e4a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:32:59.681329');
INSERT INTO "django_session" VALUES('c4f1947af0d0f0f470e14bba37bdcd8e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:02.725315');
INSERT INTO "django_session" VALUES('cd97fecb012636f9a3b56e496b3d8b1a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:05.779528');
INSERT INTO "django_session" VALUES('83dd1f1e5d98ee75c0d7ecb324921f25','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:08.848729');
INSERT INTO "django_session" VALUES('de618cf7565a32dab45bbbb8d2086e86','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:11.906906');
INSERT INTO "django_session" VALUES('542875e2310009cb69c192c8e018ebbf','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:14.954779');
INSERT INTO "django_session" VALUES('7f6241b72dc5e2e695dd65f684fe8635','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:17.998812');
INSERT INTO "django_session" VALUES('8e22190ccfd6554925ef9d0415794a21','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:21.029310');
INSERT INTO "django_session" VALUES('784622de3f94afc53fb6ad8387f584bc','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:24.087080');
INSERT INTO "django_session" VALUES('72469b81e71fcd2c1d338e8528f752d6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:27.133116');
INSERT INTO "django_session" VALUES('5cd278f3f887204b37e8ebfaa317229a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:30.218773');
INSERT INTO "django_session" VALUES('8d0776a7c403648d14408634f1d0d9e4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:33.269159');
INSERT INTO "django_session" VALUES('87b76a04dcece6c3fa2b334cea529608','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:36.314524');
INSERT INTO "django_session" VALUES('cf851e9e7edfe346afe2f21d6155b9f9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:39.359359');
INSERT INTO "django_session" VALUES('48c78380d4929ad48fd87e591f23691a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:42.415173');
INSERT INTO "django_session" VALUES('b8600e4c7d14233fd58e09409a1d7573','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:45.449172');
INSERT INTO "django_session" VALUES('de443cf9c9cb71f2f1905f0a6aa1bfed','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:51.548201');
INSERT INTO "django_session" VALUES('a7432d89253566a15eb98cad8f2543d2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:54.658152');
INSERT INTO "django_session" VALUES('7d7adfd03ce2f0d77dc0bb917b5e3008','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:33:57.775928');
INSERT INTO "django_session" VALUES('6b43e9c80ce6ee0d9e6999ba01ccd2e4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:34:00.826935');
INSERT INTO "django_session" VALUES('cd17fb941699bd993efed56173eb486e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:34:03.871988');
INSERT INTO "django_session" VALUES('b1c3fa4bf2cd81984bde7d86e8f5b2a6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:34:06.919235');
INSERT INTO "django_session" VALUES('1454045ee2a51aa82735065a8c1601b1','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:34:10.240036');
INSERT INTO "django_session" VALUES('64fcdce23dc954e5033e84533e0a931b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:34:14.432359');
INSERT INTO "django_session" VALUES('fad3d653e4345e38681dfe4d6a358bd2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:34:18.469361');
INSERT INTO "django_session" VALUES('d64d162ba115f53ee0b94525e1641dac','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:34:22.060006');
INSERT INTO "django_session" VALUES('47ad0b130832789a6657ef2d41da2c99','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:34:25.428815');
INSERT INTO "django_session" VALUES('dc7a328faf4fdc3228679551ae1567c3','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:34:29.204169');
INSERT INTO "django_session" VALUES('ef9ac3ad6ec80e04b9ff14f2afc97957','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:34:33.758628');
INSERT INTO "django_session" VALUES('4296476bbc687c9932bf533f9611bcab','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:34:39.642660');
INSERT INTO "django_session" VALUES('75f425656a65b715e6237c6c4e451eb4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:34:45.496144');
INSERT INTO "django_session" VALUES('6914df3a4ecce73420fee74ee067736a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:34:50.170800');
INSERT INTO "django_session" VALUES('72d4086a459a1fb147dec18191ad79c4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:01.311449');
INSERT INTO "django_session" VALUES('b054ba7e7ce61aaf8d9e97993754135a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:05.332661');
INSERT INTO "django_session" VALUES('4d6b13b7844e3b554b1a0ad85333ca95','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:08.712748');
INSERT INTO "django_session" VALUES('f1f40cac127f16bce3ff1f4d0faf32d9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:12.344516');
INSERT INTO "django_session" VALUES('d25ea0cef06e84a8d5fdd615d0a31ee0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:15.374994');
INSERT INTO "django_session" VALUES('5355cefdf1e6daa1f2030c2ff2d34b64','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:18.566823');
INSERT INTO "django_session" VALUES('d08de918da1e7f6a51091e5afb1b6854','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:21.706580');
INSERT INTO "django_session" VALUES('b177ebd9714cd86a9c0742e5bdfc28f6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:25.580938');
INSERT INTO "django_session" VALUES('aa8e1ce68a6113c06045cd72eb7b3ef1','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:29.032214');
INSERT INTO "django_session" VALUES('c01c4fa7da47eaa4df37f777579320e3','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:32.531639');
INSERT INTO "django_session" VALUES('c1efe0a5c1b78db152d4ba815720a479','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:36.071924');
INSERT INTO "django_session" VALUES('b924bb6c262cf09c8bde463d56111bf0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:39.548549');
INSERT INTO "django_session" VALUES('b4237987c0fcff771152ee9c9ba05fb6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:43.309960');
INSERT INTO "django_session" VALUES('d7fb57144fd54f5c7ae10fd290c7c169','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:47.072592');
INSERT INTO "django_session" VALUES('70855995b9d192bf5ac64e8efdf0d2f0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:50.293054');
INSERT INTO "django_session" VALUES('3a6fa33cdf9b98bc54e1857aa68bd347','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:53.718003');
INSERT INTO "django_session" VALUES('6b1e71a03b1a5127df8fecd93d029675','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:35:56.968383');
INSERT INTO "django_session" VALUES('4a8e7a7a161057d67cec961e7b335afb','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:00.248362');
INSERT INTO "django_session" VALUES('617cc7a9a6fcc611f00975ec653f6893','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:05.080823');
INSERT INTO "django_session" VALUES('bc2c2424b5609decfe87aebfde4cfd1b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:09.650445');
INSERT INTO "django_session" VALUES('9b8d62003e167f6bdb3674e603883d4e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:13.674835');
INSERT INTO "django_session" VALUES('80f273fa6e528b40e5408f6b509fb79b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:16.972225');
INSERT INTO "django_session" VALUES('469725ece78efb64bf64fcb30bf69fb7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:20.897566');
INSERT INTO "django_session" VALUES('7d4a5053766d7fc87c823e0794a134a4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:23.946180');
INSERT INTO "django_session" VALUES('93b63b6d48c3d996989faa79871748f7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:27.038648');
INSERT INTO "django_session" VALUES('884935f53dc7042223a48d0f91c071be','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:30.092985');
INSERT INTO "django_session" VALUES('2be1979073d2a0d4928e05496e16e0c6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:33.156548');
INSERT INTO "django_session" VALUES('84e2b4632dd5e823bbfe02c0a72390e0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:36.200221');
INSERT INTO "django_session" VALUES('8cf60e766fb9cd44b266fede7f8014b4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:39.243747');
INSERT INTO "django_session" VALUES('6921769a8bba43e55ee36163ce882907','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:42.300300');
INSERT INTO "django_session" VALUES('c78e0b63f53ab9c4c8764b4d039f1e8c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:45.334647');
INSERT INTO "django_session" VALUES('443b6307213bbf439769afde32e4020e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:48.375968');
INSERT INTO "django_session" VALUES('3d18a712108ad85372b7cb26e5ba1923','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:51.420748');
INSERT INTO "django_session" VALUES('bf948b2fb5dea5768a919bd04ceeabff','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:54.451098');
INSERT INTO "django_session" VALUES('abdf90cef9ed77136da5edbfd7fd6a37','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:36:57.497013');
INSERT INTO "django_session" VALUES('d40d14afce252df562a25b6c373c33a4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:03.748578');
INSERT INTO "django_session" VALUES('2f2dccd6ced5ea2a6bb0ddc2c3db40db','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:08.069171');
INSERT INTO "django_session" VALUES('9b590e6f8926bf28f054b16692a8637e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:11.181499');
INSERT INTO "django_session" VALUES('4f374e90df1d1d8326bb0c4bd8195be3','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:14.237332');
INSERT INTO "django_session" VALUES('ec48916092229dde04f358c40c928d62','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:20.592569');
INSERT INTO "django_session" VALUES('cff2fac4ca5fa706276e7857d3e6df67','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:23.731917');
INSERT INTO "django_session" VALUES('d9677a2715051413b517b076a11cb9ec','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:26.777469');
INSERT INTO "django_session" VALUES('44fef4cc3635001b662c42033d2c2323','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:29.822919');
INSERT INTO "django_session" VALUES('92b9daba888e48fc1da69325f1b98476','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:32.870333');
INSERT INTO "django_session" VALUES('b4ffb116d405b605ad4be906a0bf82aa','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:35.933214');
INSERT INTO "django_session" VALUES('0922e4b7b98db7fa50056239202f4280','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:38.974799');
INSERT INTO "django_session" VALUES('70cd2c31e1ea4d1ae52a7702eb5d7ff6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:42.033891');
INSERT INTO "django_session" VALUES('c9b033baa53583a570e786131dc7be1a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:45.077533');
INSERT INTO "django_session" VALUES('b53067dd6ec15b195f6811a33517f270','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:48.122718');
INSERT INTO "django_session" VALUES('e18be9c1344bbc8950b29a89f642b411','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:51.167434');
INSERT INTO "django_session" VALUES('2882e10519be11ad168cec80d2b771ad','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:54.228424');
INSERT INTO "django_session" VALUES('4cb3be6a4303395b2703fdad2ef2e578','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:37:57.273089');
INSERT INTO "django_session" VALUES('bd486d6d141f0d871074848daeee81ba','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:00.319297');
INSERT INTO "django_session" VALUES('5061b6d7c74c27c1d9e9e16927a8ec61','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:03.366092');
INSERT INTO "django_session" VALUES('6ab12adb95092240f0c29dfb17bc0a19','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:06.416265');
INSERT INTO "django_session" VALUES('6050a15eb733bb0c28c11b080637c762','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:09.454953');
INSERT INTO "django_session" VALUES('db9d97b31fe676787a1c3c01ab74b2de','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:12.498836');
INSERT INTO "django_session" VALUES('3771a507ca6183c6a9abd9ed7cb04364','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:15.547943');
INSERT INTO "django_session" VALUES('d8b1282d9ecd70e4b367623ce7572dbe','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:18.591228');
INSERT INTO "django_session" VALUES('b6be0745917e8053b5bb7ccc92599304','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:21.653039');
INSERT INTO "django_session" VALUES('051e134aea832537a6d8891fa0fecab8','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:24.701250');
INSERT INTO "django_session" VALUES('501605fe13698d08ecfd94c6694f9460','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:27.759685');
INSERT INTO "django_session" VALUES('bc821add270162cedcb8306937f569b7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:30.850037');
INSERT INTO "django_session" VALUES('9347bbf0e35e2042e199a96e50a4ecd0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:33.895083');
INSERT INTO "django_session" VALUES('e555effd748c3983fbd5507d653a0a85','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:36.929856');
INSERT INTO "django_session" VALUES('f202c4e24017e7d4eca3f15213290e77','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:40.003153');
INSERT INTO "django_session" VALUES('2a9a501c567beba820d27599af455a3e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:43.049722');
INSERT INTO "django_session" VALUES('0ef375318ce67a26af887014332e0ea0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:46.092981');
INSERT INTO "django_session" VALUES('18d74f156ac715e2a801d899ebdc3b39','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:49.143437');
INSERT INTO "django_session" VALUES('991098c016ceb87345ae6a4765f6c4d5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:52.243466');
INSERT INTO "django_session" VALUES('4f35cee2c768f8239ca22a22412ea7b6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:55.288406');
INSERT INTO "django_session" VALUES('176e4c3eb683595b151813073c269cea','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:38:58.320040');
INSERT INTO "django_session" VALUES('77e9e9413492f2df6044371b0c0219ac','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:01.365258');
INSERT INTO "django_session" VALUES('f60ffc1c99268c01100e663354a16c12','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:04.643500');
INSERT INTO "django_session" VALUES('5781d216c9ee96f980603310aebddf0c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:07.698140');
INSERT INTO "django_session" VALUES('69844203590f465e7058e9a2a434c574','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:10.745609');
INSERT INTO "django_session" VALUES('ab681ec5ea42d6fac7e6d66e254b103b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:13.790919');
INSERT INTO "django_session" VALUES('a09b5ec1eb1397987456345cf09e3fd8','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:16.852033');
INSERT INTO "django_session" VALUES('aa55709ce2671587cdd90847d8c4e476','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:19.898268');
INSERT INTO "django_session" VALUES('74507d50bbe1481f019efb8767df86d9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:22.946887');
INSERT INTO "django_session" VALUES('1d9799ea99a24c6d8e67dcd5d456fcbe','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:25.991419');
INSERT INTO "django_session" VALUES('ca9638dc74238b39392581c83ef6a755','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:29.039981');
INSERT INTO "django_session" VALUES('6a417d20d9612712ae007908cea9812c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:32.094102');
INSERT INTO "django_session" VALUES('51e3124bb0028acbc52b4dfbf5e9b677','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:35.140909');
INSERT INTO "django_session" VALUES('f64fe3bf37c161b3ad94bf7499cb16f0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:38.189820');
INSERT INTO "django_session" VALUES('2490b115ae06013f80643b27af4fe806','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:41.245044');
INSERT INTO "django_session" VALUES('9a778cd97bf4b8ff27d858cce1337cbb','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:44.294093');
INSERT INTO "django_session" VALUES('4e5efafd92b548b281e70b4fe0e1778e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:47.336688');
INSERT INTO "django_session" VALUES('aa51a84a95923fa769601f26db9de189','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:50.381828');
INSERT INTO "django_session" VALUES('e32c7550beca424b26b68717c7b0458e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:53.428301');
INSERT INTO "django_session" VALUES('b18e21309489bfd59fed72709be9d9d6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:56.472447');
INSERT INTO "django_session" VALUES('0a8b826c7612316b832de0cb523afcfe','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:39:59.518474');
INSERT INTO "django_session" VALUES('2c493a6e6dbe3df2a66cec8238400a90','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:02.564098');
INSERT INTO "django_session" VALUES('c2fe2a5ff99f846d61456bfd4d8261ac','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:05.608712');
INSERT INTO "django_session" VALUES('cb4d6078d814c41f925597d043727ae0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:08.640833');
INSERT INTO "django_session" VALUES('452c9d80b1abf3dc32e8953a41a6d897','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:11.671483');
INSERT INTO "django_session" VALUES('1598f64b14b7d927f79b18cd21ae91e2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:14.748996');
INSERT INTO "django_session" VALUES('2e105d64b0730c614dcc0c3aeeacece4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:17.791746');
INSERT INTO "django_session" VALUES('11d23b626f02bc17263ad0fb98b80f35','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:20.867334');
INSERT INTO "django_session" VALUES('94a28c822c83e2b74d13dd984297baae','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:23.913585');
INSERT INTO "django_session" VALUES('67de065e91c55e5895fd314095910c27','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:27.000182');
INSERT INTO "django_session" VALUES('7fdf87d4770f390ddf9b156dd3a5febc','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:30.045767');
INSERT INTO "django_session" VALUES('4466928c9d2783d8819feacc59bc2857','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:33.090166');
INSERT INTO "django_session" VALUES('8074d1dbf6460198d508656922f64941','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:36.135053');
INSERT INTO "django_session" VALUES('460fc509602437035162080d5cf12c44','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:39.179571');
INSERT INTO "django_session" VALUES('f70503c0f9bdafe8889e378c34a46c66','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:42.213521');
INSERT INTO "django_session" VALUES('5fb58784725e7e9cbaadb2113203da0e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:45.253106');
INSERT INTO "django_session" VALUES('1a8974b5b390d9bb7729fb93f2953d5e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:48.298851');
INSERT INTO "django_session" VALUES('ea4fc1f6a6a1fe7835e09a316a819a2a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:51.346405');
INSERT INTO "django_session" VALUES('be40081738b514e79d6899b19b133618','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:54.393803');
INSERT INTO "django_session" VALUES('c3c9426b2cd38736c5152c35b3092bae','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:40:57.546788');
INSERT INTO "django_session" VALUES('0e68f4890b2790bc967b3cd4cb410e7d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:00.595526');
INSERT INTO "django_session" VALUES('6fa244c73de0bc9c4c05137c53a3f0b9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:03.663195');
INSERT INTO "django_session" VALUES('5a1fe59dc76f11cf487767291b403c2b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:06.710433');
INSERT INTO "django_session" VALUES('5e8befbb3f84662bcdcb9b6e6ae0d38c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:09.757787');
INSERT INTO "django_session" VALUES('ce0b527844d6587b49be70f7d635f288','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:12.802996');
INSERT INTO "django_session" VALUES('106202335629e6ff9afadb96fe07dfac','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:15.845016');
INSERT INTO "django_session" VALUES('40de612a8cf598319d82cff1137bd9eb','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:18.910956');
INSERT INTO "django_session" VALUES('e7d8503bc282b8230eae69b5af121820','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:21.966589');
INSERT INTO "django_session" VALUES('a82e838b82c92fe862470bb3962fd316','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:25.009468');
INSERT INTO "django_session" VALUES('a0c3bdb61dd997682b74434376eb0146','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:28.062656');
INSERT INTO "django_session" VALUES('53a69da8a7e69b9541fcf374d0a32fc9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:31.159065');
INSERT INTO "django_session" VALUES('e0a3ac5d42f2d4c693965cab86cc6a8d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:34.205200');
INSERT INTO "django_session" VALUES('2a727f61c2c93753c364e86135cb804d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:37.247698');
INSERT INTO "django_session" VALUES('17d8b8ca51714c0d38528d0378bfa79c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:40.323955');
INSERT INTO "django_session" VALUES('8fe5920696f105e7be781cd059399abe','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:43.515694');
INSERT INTO "django_session" VALUES('60a94d5c415e1f368acf461d2e04b277','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:46.564812');
INSERT INTO "django_session" VALUES('adfbc862f3f963aa04864022894b2823','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:49.640821');
INSERT INTO "django_session" VALUES('e60cc6d13349b70a0611cc75aefce382','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:55.646459');
INSERT INTO "django_session" VALUES('834a34e1d2b07c7a64047f2da51a0c2a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:41:58.702173');
INSERT INTO "django_session" VALUES('3b0ebf4a2e8c3e8c9aa7014d7df40009','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:01.747994');
INSERT INTO "django_session" VALUES('6a306da4e8d9deb71b77139ecc0289ab','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:04.787521');
INSERT INTO "django_session" VALUES('7efabb9be623b21ac7237fe45bd2ab01','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:07.847167');
INSERT INTO "django_session" VALUES('38bfb727e01e0df161c488894f806e55','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:10.891157');
INSERT INTO "django_session" VALUES('f45f6d37a4844375bb987f9a3df8a2e9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:13.939285');
INSERT INTO "django_session" VALUES('0dee2cabd75618478c527f26c6d5a063','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:16.984653');
INSERT INTO "django_session" VALUES('9fb424f12d49de4fb9d22bf9925e7a73','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:20.017385');
INSERT INTO "django_session" VALUES('266e6ffca4677e075c860ff8245accdb','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:23.076897');
INSERT INTO "django_session" VALUES('8e83c0c619cdfb37f823fdde4cdd3c52','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:26.153149');
INSERT INTO "django_session" VALUES('178b33caca8a3b7cfdd11fff0c1e9e11','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:29.212814');
INSERT INTO "django_session" VALUES('0cbc11eba05dfa423a3361e26a52c1ef','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:32.272863');
INSERT INTO "django_session" VALUES('55946c5792b6ed9ee21f366eed98a4c7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:35.320015');
INSERT INTO "django_session" VALUES('711c28008767c005337af20df103597f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:38.392969');
INSERT INTO "django_session" VALUES('59a5c8b0230306f3e29a42d361ef4080','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:41.457414');
INSERT INTO "django_session" VALUES('37fbb8f997267956a5ca420517390fab','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:44.498999');
INSERT INTO "django_session" VALUES('59e962f61f01a214d63bb46dfa50d2fc','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:47.545842');
INSERT INTO "django_session" VALUES('152aff26aae98cedc31258725222572f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:50.590169');
INSERT INTO "django_session" VALUES('f36929424971279b218b7eebd5011ec2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:53.636302');
INSERT INTO "django_session" VALUES('427fc889a43825c803f9a8ea088ee3ac','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:56.696379');
INSERT INTO "django_session" VALUES('648c3f0174da3ff3b556d87ba4464eff','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:42:59.745588');
INSERT INTO "django_session" VALUES('400c57c4cb0f0919c25e2d8dea9eccc9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:02.812400');
INSERT INTO "django_session" VALUES('d6aac3e80d29fc351c1c741c839f1bbf','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:05.850039');
INSERT INTO "django_session" VALUES('35d1dc84c7876c6d6639f0e9da4d31db','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:08.893407');
INSERT INTO "django_session" VALUES('34ce02ea392940584084e263bcd3c911','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:11.943641');
INSERT INTO "django_session" VALUES('a5be985e50becc2cc89abf9142cee261','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:14.978465');
INSERT INTO "django_session" VALUES('be04e33cf9a2ebbe3d91bddf9e57c700','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:18.021946');
INSERT INTO "django_session" VALUES('418d3d22132456fbbe340b8c068b659b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:21.066722');
INSERT INTO "django_session" VALUES('71dc168dd2f602567d7a07733dcbcbcc','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:24.103177');
INSERT INTO "django_session" VALUES('60f0746bad6975c07b5b4f4c9f9b63e0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:27.347573');
INSERT INTO "django_session" VALUES('b1dd92a0caac7ec5c40fbda2dedf6b72','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:30.404011');
INSERT INTO "django_session" VALUES('462042cf4b90174f64be11051be54210','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:33.459375');
INSERT INTO "django_session" VALUES('fc340cf4bf56cadd79bb4b1a2aa64055','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:36.502932');
INSERT INTO "django_session" VALUES('37e0518efc4c3f9fb2d0556b497db155','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:39.548157');
INSERT INTO "django_session" VALUES('a31c89cf21efc41baa823de2dda617c0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:42.594237');
INSERT INTO "django_session" VALUES('85f4df4d27cdd89855a2d05fa8350462','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:45.638434');
INSERT INTO "django_session" VALUES('05e885b0733bc3a41e677f62227518b8','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:48.667808');
INSERT INTO "django_session" VALUES('dd2f6e7c496a7c60201332391891342f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:51.712815');
INSERT INTO "django_session" VALUES('74d6c3037e4f53c41ee5bf99c43239bb','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:54.774139');
INSERT INTO "django_session" VALUES('543c973c1c6e7849693d4c1a3f7aa215','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:43:57.820004');
INSERT INTO "django_session" VALUES('4834e002e0474f798e2d0bb50894467e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:00.867369');
INSERT INTO "django_session" VALUES('a00b40d9e09ce7b6dcfb1d5daf84eae8','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:03.910839');
INSERT INTO "django_session" VALUES('a05e5a01b446b6cfda48befae3cc6225','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:06.956838');
INSERT INTO "django_session" VALUES('fcebae0f83a813f676ea0276ded07a40','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:09.999459');
INSERT INTO "django_session" VALUES('5cd4e4a9c236256027707b545266fb51','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:13.075229');
INSERT INTO "django_session" VALUES('c7372fc38c96bfa96168c710c4fd0976','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:16.136962');
INSERT INTO "django_session" VALUES('c8216e6f70a6432483ff27cf6502d3c0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:19.226687');
INSERT INTO "django_session" VALUES('3b66a0d38a569e78fa193f7f207f77da','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:22.268747');
INSERT INTO "django_session" VALUES('4717a84b1c9079502135aa532165fbf3','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:25.313552');
INSERT INTO "django_session" VALUES('90d6b8b06ef3e4e999fae2e29d83fb3d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:28.360738');
INSERT INTO "django_session" VALUES('bdd38ebbf8298473f56adcc9e98592a2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:31.536989');
INSERT INTO "django_session" VALUES('f581eda2f0b5a946cfbcb80ea027adfd','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:34.713140');
INSERT INTO "django_session" VALUES('c995f12a9f8522c5190796c65a8fcdfd','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:37.760052');
INSERT INTO "django_session" VALUES('3ff133894747706520d80a6adf412597','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:40.801907');
INSERT INTO "django_session" VALUES('9ea0ae97eaf99b9d94fc7166963581ce','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:43.845934');
INSERT INTO "django_session" VALUES('0b7b65dcb2d8e60c14338757c372e7c7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:46.890023');
INSERT INTO "django_session" VALUES('5bd3b801078a6faab74ec963259a5e3d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:49.941253');
INSERT INTO "django_session" VALUES('ffb447b50de035df1a7d3edf70e268cd','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:52.973867');
INSERT INTO "django_session" VALUES('afe6c666706c7439e9eb3ace1aea5d1b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:56.017541');
INSERT INTO "django_session" VALUES('d70c856cadf6b1409ef21b94b16c1f0a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:44:59.175159');
INSERT INTO "django_session" VALUES('5587843789ca11cffa7eefd148ed487f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:02.224585');
INSERT INTO "django_session" VALUES('012bca968f5c949cf1f675a67c9b39b2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:05.264320');
INSERT INTO "django_session" VALUES('1f5e9cb96ab972af3050cf1286a47752','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:08.312168');
INSERT INTO "django_session" VALUES('c0a4ba1667bdcafb1dc5a92c501a251f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:11.357909');
INSERT INTO "django_session" VALUES('ab64942656a13c4fae373bf947f606e5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:14.406464');
INSERT INTO "django_session" VALUES('daee048c1f791e1031809e6ca031c44c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:17.465040');
INSERT INTO "django_session" VALUES('ecbaff681cae3285fbb0bc4f333a1745','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:20.510749');
INSERT INTO "django_session" VALUES('0e384987a300a515eec4901c6fbdf561','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:23.556324');
INSERT INTO "django_session" VALUES('3ea49a19af97e96382e2accc2f06be6a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:26.601423');
INSERT INTO "django_session" VALUES('40bd6227eb9e0b815f63aa667b427c8a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:29.643474');
INSERT INTO "django_session" VALUES('61e25ffcbdb9fb476a4c6e3689777799','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:32.690331');
INSERT INTO "django_session" VALUES('454c7500fbeddfb0e6db4eede58c8f90','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:35.737330');
INSERT INTO "django_session" VALUES('ed7f96a4cf039960cda67396c97c2e64','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:41.817772');
INSERT INTO "django_session" VALUES('970f9ff17cb3edd3980c3d59cbc66795','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:44.945469');
INSERT INTO "django_session" VALUES('f47f35cf731e64a616597be82ecc40ca','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:48.008844');
INSERT INTO "django_session" VALUES('5b6658e9a3e6d27bd3eec0f824ddab71','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:51.062839');
INSERT INTO "django_session" VALUES('b530327f817babe0ac48b4b3e479b2d8','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:54.129781');
INSERT INTO "django_session" VALUES('cac2450df8883d0d023ab3d51f50d22d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:45:57.253712');
INSERT INTO "django_session" VALUES('1b0e3cd884d0143b6e38095152204fed','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:00.300569');
INSERT INTO "django_session" VALUES('40ab87761e4a1b9fbed49e1ea89c5c50','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:03.338198');
INSERT INTO "django_session" VALUES('7fec32accbb02e3ef10629d80c72874b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:06.389338');
INSERT INTO "django_session" VALUES('607826fbe3652f2699add3a9ffa01b13','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:09.449194');
INSERT INTO "django_session" VALUES('1ca2da4bc8e290d7e3d74ab52fc4ddd8','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:12.552261');
INSERT INTO "django_session" VALUES('076ae2f1c9b1cff0098bd7b94cb5f2c9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:15.604223');
INSERT INTO "django_session" VALUES('b4ec9450b4415823410b581a883545f9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:18.644065');
INSERT INTO "django_session" VALUES('44bf5c5eb811adf82ce5e01f60046f00','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:21.692562');
INSERT INTO "django_session" VALUES('8da28e8e0b84c49ef7c406c3bd42ba73','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:24.723869');
INSERT INTO "django_session" VALUES('eb066cc719c69d586b74c137ca2ff1a0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:27.837929');
INSERT INTO "django_session" VALUES('2130e7f521b6e41aa3505ad3e31672e1','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:30.886243');
INSERT INTO "django_session" VALUES('4e3024accd0d5f17646b3456e51a8e30','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:33.936765');
INSERT INTO "django_session" VALUES('a0ad8a3f884555b4def3090618117629','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:37.320175');
INSERT INTO "django_session" VALUES('57a1b52970fba04f1403c1c79a4d8808','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:40.364574');
INSERT INTO "django_session" VALUES('f96132236b8999f939b1636e74ddb4b5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:43.734881');
INSERT INTO "django_session" VALUES('b8356e834afe1c703dbacee2e621b0e5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:46.824318');
INSERT INTO "django_session" VALUES('0ca56f4c07811afc243d203351a63f0d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:49.869016');
INSERT INTO "django_session" VALUES('2cfed48ed34c523e8e56b12947f44083','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:52.916213');
INSERT INTO "django_session" VALUES('99aef45338485b15c5ff0805f95805b9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:55.958583');
INSERT INTO "django_session" VALUES('7ad3ea3bcae354fb5f7303359837933e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:46:59.020919');
INSERT INTO "django_session" VALUES('6a12496e671038500ead1e2d3331d2f3','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:02.093415');
INSERT INTO "django_session" VALUES('41df680924b4c381ef887f854c93db6c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:05.150294');
INSERT INTO "django_session" VALUES('aeac6237925def4a8365465e840d821d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:08.196356');
INSERT INTO "django_session" VALUES('4cce8888d59ad03e0dfcf60105cfc9cb','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:11.226256');
INSERT INTO "django_session" VALUES('b33fbc7d27f7342a6a300eda9e2ca364','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:14.347875');
INSERT INTO "django_session" VALUES('33d643fea59cb12c31a4bb3d55c27f79','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:17.392604');
INSERT INTO "django_session" VALUES('c283a9baced5537c0ddbac3d89e3d36f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:20.435691');
INSERT INTO "django_session" VALUES('db3d6993feee6eff8dba98bf36e6c43a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:23.483539');
INSERT INTO "django_session" VALUES('999689de43dfffc4a404ec78a46251be','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:26.531116');
INSERT INTO "django_session" VALUES('3a355845ebb38a56427b1e4af4299fae','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:29.575336');
INSERT INTO "django_session" VALUES('c500760718719e8d0f133a05b5f4b28b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:32.622457');
INSERT INTO "django_session" VALUES('8c9118c436747314d96c342f1ce7717f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:35.682960');
INSERT INTO "django_session" VALUES('62733d15f4853ce749572ff86f1336cf','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:38.729271');
INSERT INTO "django_session" VALUES('ae11acb2f30cdabfd0ce9eec1f72e2fe','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:41.771491');
INSERT INTO "django_session" VALUES('66b134f94b2ee0e8e48d09cd7d4b3655','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:44.817463');
INSERT INTO "django_session" VALUES('3e7f8460a4230f547d665f3f3c0310f9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:48.186697');
INSERT INTO "django_session" VALUES('bd6129e0d4fa193a833ff69256027408','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:51.230819');
INSERT INTO "django_session" VALUES('83e581162898de0908ef5aebe68a2936','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:54.275518');
INSERT INTO "django_session" VALUES('1f630037871755ea9fc49b9951384f4c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:47:57.323143');
INSERT INTO "django_session" VALUES('1d169eb85addde3cc3221f444dbe132f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:00.372800');
INSERT INTO "django_session" VALUES('0e0e03efe537a355f100ce24a9d4c3ab','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:03.413087');
INSERT INTO "django_session" VALUES('a4f183c984cb75a9ea3642b6954e3c3f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:06.458755');
INSERT INTO "django_session" VALUES('eba8cc561b443bae158290e503d05c0e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:09.517412');
INSERT INTO "django_session" VALUES('9726d54f6738df90e371d1456e50a7af','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:12.561653');
INSERT INTO "django_session" VALUES('f6d0d3d0a65c51281c8b5a87d87a8111','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:15.607633');
INSERT INTO "django_session" VALUES('a3c0361ed017db4214cac9a368b15c48','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:18.653980');
INSERT INTO "django_session" VALUES('e8fd384eea6d81884ebd41a12662fe14','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:21.727495');
INSERT INTO "django_session" VALUES('f8fe16de7440fe0b8f04de1875b7e016','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:24.773765');
INSERT INTO "django_session" VALUES('7606d2787085fb1bffa7196408e2d005','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:27.820765');
INSERT INTO "django_session" VALUES('d4c7240482239994b652736e401be5a9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:30.853920');
INSERT INTO "django_session" VALUES('5a572a2ac9d62f56ebe7789f6b284052','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:33.898542');
INSERT INTO "django_session" VALUES('7016a263746f6c13b4f21ef7673df816','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:36.946860');
INSERT INTO "django_session" VALUES('31ccb33e90ae0a4fbb0275c5fc13635c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:39.992622');
INSERT INTO "django_session" VALUES('4eb9edf68dcfc911791fb1e2bbde7c9b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:43.030120');
INSERT INTO "django_session" VALUES('5343662531cc8f439b72ad0ea11d5ce6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:46.070248');
INSERT INTO "django_session" VALUES('5c4ffdd634f6cc1713b3b2574daef80f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:49.117678');
INSERT INTO "django_session" VALUES('12c09a91d5d1ab2e36134ad207099e9e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:52.164104');
INSERT INTO "django_session" VALUES('c97e969e2c53c68b39d2f3b6b5bc7fb2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:55.198991');
INSERT INTO "django_session" VALUES('7bfbd8665f7d325e71f414dcfacd6359','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:48:58.245583');
INSERT INTO "django_session" VALUES('5adc52ce25295982ee0388b4498ad159','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:01.291099');
INSERT INTO "django_session" VALUES('0768cedfb6a1649d73c7aca6c643e4e4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:04.554402');
INSERT INTO "django_session" VALUES('5051daf4168c19f7ee56ada95883e52d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:08.086145');
INSERT INTO "django_session" VALUES('d7286ba1374f634a520c197292615a2b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:11.124560');
INSERT INTO "django_session" VALUES('ef6211dd1ca54e471e9eaee4e35ae6da','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:14.169919');
INSERT INTO "django_session" VALUES('d36376583ff687574bb4f6018cf5fa8c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:17.213295');
INSERT INTO "django_session" VALUES('bc76147b277a48305184011f0ca1de22','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:20.271252');
INSERT INTO "django_session" VALUES('9bc11c05cfc5d0a15fbbae4cc2b0a86b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:23.318228');
INSERT INTO "django_session" VALUES('0eed50cd0c9691a530e07464bbe63351','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:26.363904');
INSERT INTO "django_session" VALUES('d862798bd497a3c4af863e95930cf0b4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:29.406949');
INSERT INTO "django_session" VALUES('b27384e904e15d952d4c7c727485976a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:32.452828');
INSERT INTO "django_session" VALUES('dcfb0f12279e0012871b6f9d9640e64f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:35.484206');
INSERT INTO "django_session" VALUES('9bc8cc6a2fc0ad6d773370052f5cbb0c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:38.528406');
INSERT INTO "django_session" VALUES('ab7e6400c90a79c0a3346a17ec35e81e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:41.652446');
INSERT INTO "django_session" VALUES('47455f80b1663f7a0d25b7498c2b7009','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:44.723633');
INSERT INTO "django_session" VALUES('01c6b88a37e402dfd589ce51ba0dbf86','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:47.762627');
INSERT INTO "django_session" VALUES('016e607b22a5c227ea8c70f7e7df8181','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:50.794325');
INSERT INTO "django_session" VALUES('7af77d47139e445e89b08efdc5a31640','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:53.837279');
INSERT INTO "django_session" VALUES('ae6cbe92e106ba0eb4b0ffcf9c0ba41a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:56.884427');
INSERT INTO "django_session" VALUES('8c854872bf9725ef2c8bda7ee11c006c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:49:59.929657');
INSERT INTO "django_session" VALUES('affe2a69e3d3b4979f964e02d9304dfe','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:50:02.974385');
INSERT INTO "django_session" VALUES('0aaf043e705c56dec2a5d2b028347ebb','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:50:06.017966');
INSERT INTO "django_session" VALUES('d593c2e99a14dd9dc5ea45b33a586bda','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:50:09.139077');
INSERT INTO "django_session" VALUES('a234ad3991fda1adeef4b03a744f4c69','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:50:12.371984');
INSERT INTO "django_session" VALUES('a0ee8e6386004719b915cae2331cafc7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:50:15.580931');
INSERT INTO "django_session" VALUES('2a8d0766fbd40e91f276e46788ae79ef','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:50:19.606311');
INSERT INTO "django_session" VALUES('bac004e6cdc64bb1bc050bac0d38b220','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:50:22.856129');
INSERT INTO "django_session" VALUES('3a6fe23cc1feac4e006351f32800c7d2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:50:26.266552');
INSERT INTO "django_session" VALUES('42602d76f1785d5e50f4dd7f61aadb12','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:50:36.304976');
INSERT INTO "django_session" VALUES('2a5dbb2fc3adb9a9ec76503612359fd1','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:50:39.517075');
INSERT INTO "django_session" VALUES('21dc08e7504627b602afef21c025b2de','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:50:43.489347');
INSERT INTO "django_session" VALUES('5d565b6f87b9c5a7b0dca0df6c9cdc18','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:50:47.301965');
INSERT INTO "django_session" VALUES('621ea1d2e2bbf841e6c200b3ae168f2e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:50:50.478652');
INSERT INTO "django_session" VALUES('72f8cf8725e47cae9df974f7f4c7b9f9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:50:54.491271');
INSERT INTO "django_session" VALUES('20a3e192bb1a62b7522f42d2bcbd5466','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:51:02.498595');
INSERT INTO "django_session" VALUES('0d205d4531be10a2fb717e619e967b63','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:51:06.817222');
INSERT INTO "django_session" VALUES('cf430b94c54acba9b4b28809b5ceabc8','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:51:13.843013');
INSERT INTO "django_session" VALUES('5d060bcb059277b5a50b63c179ab1c24','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:51:18.133887');
INSERT INTO "django_session" VALUES('5a8c65b10f42df42d6669ab17fa6ae1d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:51:21.356810');
INSERT INTO "django_session" VALUES('20a4e2b1f6cd0156e2bc4c83ce6693cf','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:51:24.635666');
INSERT INTO "django_session" VALUES('f712a6d055e226cef9829b24b429223b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:51:27.679976');
INSERT INTO "django_session" VALUES('d33ce299ec095ab5b5d17fe054e2349d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:51:30.725653');
INSERT INTO "django_session" VALUES('0807355c4347531e31225f3fdaf153e1','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:51:33.768363');
INSERT INTO "django_session" VALUES('0c404ad1d0ab64d03bf027ad71a2c129','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:51:38.641117');
INSERT INTO "django_session" VALUES('f14ba713255f9789c9f2538009fdc1cf','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:51:42.630082');
INSERT INTO "django_session" VALUES('f1ae4c284fa1d7c31a34e1a7e2747d1b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:51:46.301843');
INSERT INTO "django_session" VALUES('06da95aadc1929c28bbb68ec5e74887b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:51:57.644441');
INSERT INTO "django_session" VALUES('2948cc278a3cb31dd0295299ee96233b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:52:03.144313');
INSERT INTO "django_session" VALUES('61f9ed230079af8fbf689dee212b733b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:52:06.320511');
INSERT INTO "django_session" VALUES('22c716472d2fca95e5381f0c77e8c854','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:52:09.463315');
INSERT INTO "django_session" VALUES('99f099c57c5085502ef0c86628b870bb','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:52:12.779634');
INSERT INTO "django_session" VALUES('d7d1f92befc57c0fb224ad1b34f555f9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:52:15.830145');
INSERT INTO "django_session" VALUES('19cf3070ee1755ccbe61301e980e4159','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:52:19.124330');
INSERT INTO "django_session" VALUES('95121564edfa24e661fd807ed7dfd849','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:52:22.493700');
INSERT INTO "django_session" VALUES('d86791487aaa140603caedb75bf892b8','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:52:27.077551');
INSERT INTO "django_session" VALUES('d8a5134b609012bad254cd62f4a15662','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:52:34.620207');
INSERT INTO "django_session" VALUES('3092207fe77088bbf15ed93ba5a5e7aa','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:52:37.666697');
INSERT INTO "django_session" VALUES('ce8e42354ba1ee0922134231776f11d5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:52:43.163737');
INSERT INTO "django_session" VALUES('d9235e6c3301dc3e8f60fb4dd606191c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:52:48.721386');
INSERT INTO "django_session" VALUES('ebff5d5241448269ddc4069d7d60fc9e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:52:51.786655');
INSERT INTO "django_session" VALUES('22566888904a1ee136055d5cb48547f6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:52:54.833297');
INSERT INTO "django_session" VALUES('028ebe2004e014242f7523c937a6d805','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:52:57.877176');
INSERT INTO "django_session" VALUES('89d66a8f619c30548280693fd6465ae9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:01.159915');
INSERT INTO "django_session" VALUES('581c8540044c63d2912675c0c7e91eb9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:04.576415');
INSERT INTO "django_session" VALUES('44b445c72020f1e5439165f44a62a6ad','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:09.355575');
INSERT INTO "django_session" VALUES('1e8f9237367a2567f609b8b39f284de3','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:12.394917');
INSERT INTO "django_session" VALUES('234688211ea53636bb1079b865e1de94','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:15.452997');
INSERT INTO "django_session" VALUES('38449da9f4fbb1b5fd56fa1c74678b3c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:19.395427');
INSERT INTO "django_session" VALUES('ede683572b0f25d1a9ac22c5bab98f7d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:22.436950');
INSERT INTO "django_session" VALUES('3057a1696e193f5b9d79d6020ba61ca6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:25.817673');
INSERT INTO "django_session" VALUES('d3d8e8d835549c2f999b304ffffd155d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:28.862012');
INSERT INTO "django_session" VALUES('5ce3165363e1ecc1a9c23c302261a7bc','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:31.909266');
INSERT INTO "django_session" VALUES('1549d0222c5884cf510b969ea545887d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:34.953822');
INSERT INTO "django_session" VALUES('81f6a5a6394daf899d1f7f1838e63837','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:38.000568');
INSERT INTO "django_session" VALUES('98421c86ee7789f1ba18cbbfdbdb2245','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:41.089008');
INSERT INTO "django_session" VALUES('6acddd0863b554423dbd7164b5b1c452','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:44.239606');
INSERT INTO "django_session" VALUES('cfc8fa24ed5a0d36c5ccb708939b2eea','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:47.413035');
INSERT INTO "django_session" VALUES('7418e59423cb1b83a3195847fbd96bdc','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:50.472205');
INSERT INTO "django_session" VALUES('b586dee50deb4770d32c3fb19497771a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:53.517770');
INSERT INTO "django_session" VALUES('b13b9e0934bba5966c977415ec826a01','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:56.559908');
INSERT INTO "django_session" VALUES('13a4af3f9cc75c859a7b556bface8366','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:53:59.605274');
INSERT INTO "django_session" VALUES('5531c8d290a91ade447ef792b3bafdab','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:02.648520');
INSERT INTO "django_session" VALUES('61acf32e4b5da84449c78dd238018151','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:05.697910');
INSERT INTO "django_session" VALUES('426d9411201caaa27845afbeb34a7079','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:08.741195');
INSERT INTO "django_session" VALUES('6eb854828a16a8f69e9000da76b2b48b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:11.795005');
INSERT INTO "django_session" VALUES('807a9b1f56e8b73b03d87a2d2962549b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:14.840895');
INSERT INTO "django_session" VALUES('37b5511e465299655f3ec9ef1c65f20d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:18.208931');
INSERT INTO "django_session" VALUES('e40a6241f704de9e9ddb1d2693f5fad6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:21.356096');
INSERT INTO "django_session" VALUES('a27fb0ea6bf8754a76f49baab86b29e5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:24.402438');
INSERT INTO "django_session" VALUES('ee50aea156dae28807002212dcd97d64','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:27.446813');
INSERT INTO "django_session" VALUES('d0a9980db84b035fc171f0f6c11905e4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:30.519667');
INSERT INTO "django_session" VALUES('cc2a72de18d24a6e6dc4ea6af826bf00','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:33.549410');
INSERT INTO "django_session" VALUES('c0e2e5a89f8d68f754fea3124c094fc7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:36.594191');
INSERT INTO "django_session" VALUES('c7882cb0a0f59150d206b2ed5a4c91d5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:39.656964');
INSERT INTO "django_session" VALUES('6f46410712a65c2323fddfc0a148d9eb','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:42.702039');
INSERT INTO "django_session" VALUES('f2f6c789df469fb13122e5e30d1ab869','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:45.877543');
INSERT INTO "django_session" VALUES('3f50ff34516907016e6790078dce70d3','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:49.203396');
INSERT INTO "django_session" VALUES('3549cc0e020135bedae93976211eb18f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:52.260707');
INSERT INTO "django_session" VALUES('fa7e7417cef60e0e6d73d15e2480afd7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:55.304524');
INSERT INTO "django_session" VALUES('842a865326ad09d779b5d05867745c3e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:54:58.352434');
INSERT INTO "django_session" VALUES('4dd2e118b47376fcc07eba1ffd56eccb','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:01.410158');
INSERT INTO "django_session" VALUES('1a1ebfe32ed330ca96d0b8c9183000d5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:04.469146');
INSERT INTO "django_session" VALUES('f628f03171824bd26bdfce1424a38eb0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:07.512215');
INSERT INTO "django_session" VALUES('52ee9017c7b4913508a6faddece7f3c6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:10.627058');
INSERT INTO "django_session" VALUES('1da5b0dba93efce726be53d2fd4969ee','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:13.680790');
INSERT INTO "django_session" VALUES('bdb028de2837c4bdd1ac8459a342834e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:17.035995');
INSERT INTO "django_session" VALUES('e73a715ea57cb58ec34d1981c14176eb','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:20.093127');
INSERT INTO "django_session" VALUES('65846927419388aeab71bb488d54654c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:23.135933');
INSERT INTO "django_session" VALUES('75502e6e93ebf3b8c07134ecbe1f157d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:26.184021');
INSERT INTO "django_session" VALUES('fc1a179fa0f2522cbd6218a3eb521bd5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:29.228868');
INSERT INTO "django_session" VALUES('ed7df9ffc0bc55baa54aaff1312b8892','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:32.302934');
INSERT INTO "django_session" VALUES('a31e72ac4f6cf2e133e70d83f8040f32','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:35.346155');
INSERT INTO "django_session" VALUES('13792b400d215330cab930ceddc21e41','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:38.405667');
INSERT INTO "django_session" VALUES('46817acd4bc01e7b499565c26b9b6df7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:41.466348');
INSERT INTO "django_session" VALUES('51bd430bad124035a22533be8d2f09ae','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:44.574305');
INSERT INTO "django_session" VALUES('b6e511a811e7df683be23015f3aaaabd','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:47.622715');
INSERT INTO "django_session" VALUES('6ebdf4deb783d4f149563e0e1794b51a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:50.681488');
INSERT INTO "django_session" VALUES('6b5da6b41792ed77502244ae31ed3930','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:53.739756');
INSERT INTO "django_session" VALUES('924594b1c89489f27a72d4077ecdd26e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:56.789007');
INSERT INTO "django_session" VALUES('1ab11e02f46b08d1dfe9df1cd2950742','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:55:59.835204');
INSERT INTO "django_session" VALUES('c8dfcc1b76688e6d5941f9cc961b7f2d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:02.880813');
INSERT INTO "django_session" VALUES('ec18e075157d737fd05b6b5d9ae917aa','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:06.114887');
INSERT INTO "django_session" VALUES('65a3dbce0114412ddab07db8aa593e02','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:09.162378');
INSERT INTO "django_session" VALUES('faca35851ed97c9f29e073d9710c2400','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:12.208887');
INSERT INTO "django_session" VALUES('6a99ede5e7eae8381f6e06d0d399e6dd','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:15.270324');
INSERT INTO "django_session" VALUES('e063fbf4a43f5ef0990e4f9361440ddb','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:18.330179');
INSERT INTO "django_session" VALUES('9fa63a93b9540207afd0a4a352ab3332','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:21.698324');
INSERT INTO "django_session" VALUES('0c47db8061878751c4ce6def64269f0b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:24.757294');
INSERT INTO "django_session" VALUES('784e603542d96cca79873080a336fae6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:27.826124');
INSERT INTO "django_session" VALUES('3612123b1571061858a4845f09498cce','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:30.866319');
INSERT INTO "django_session" VALUES('6b12b0ed4baec138693d9d6fea8a17f2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:33.908632');
INSERT INTO "django_session" VALUES('530ae61e3bd9f881f961954cc68f0531','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:36.941646');
INSERT INTO "django_session" VALUES('4500c77d562b4331c1ad8ae36d3b51dd','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:39.987335');
INSERT INTO "django_session" VALUES('022b4c325d36a9d66ca887f290ba189f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:43.030428');
INSERT INTO "django_session" VALUES('42bc6ba1e67f17bab3c315bc02709ff0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:46.076618');
INSERT INTO "django_session" VALUES('f60331bb93940c84d9ea5e617236438f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:49.109127');
INSERT INTO "django_session" VALUES('61ee53f5e4e630fc845674247638a519','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:52.154316');
INSERT INTO "django_session" VALUES('3b93937800602462e64d21e44484c54b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:55.391189');
INSERT INTO "django_session" VALUES('16c45d2e30d35c63d110addc22c2b0f9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:56:58.435975');
INSERT INTO "django_session" VALUES('cbe775bf06dba52df3f7368bc8f3824f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:01.501083');
INSERT INTO "django_session" VALUES('d9921b6e449b6f4136fef7be3b0a45c2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:04.629839');
INSERT INTO "django_session" VALUES('e6762894a599795372534376752e26e2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:07.675512');
INSERT INTO "django_session" VALUES('214c327e863bed4afe92928d03b6f2c4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:10.735108');
INSERT INTO "django_session" VALUES('19481f90a18c3996a2d284cb9cc1a77a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:14.131280');
INSERT INTO "django_session" VALUES('945c903abd843010b31e91492b58d6c2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:17.180693');
INSERT INTO "django_session" VALUES('d91bd10bdd281d821864572d7f6d5473','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:20.225412');
INSERT INTO "django_session" VALUES('44ae7d2def3cc4a0ceff5fbe10d4e80d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:23.287126');
INSERT INTO "django_session" VALUES('99c3b0ccc3ae0d0c9bffef85b619f9ce','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:26.349082');
INSERT INTO "django_session" VALUES('9317b70ede3b32ecd4305f62feee05aa','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:29.407683');
INSERT INTO "django_session" VALUES('b3dbe169cb31676c3be87717dd9e762c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:32.497240');
INSERT INTO "django_session" VALUES('5818b34377233e8ac4a3238eca18e728','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:35.542416');
INSERT INTO "django_session" VALUES('bf7406d49342c7250073fd9bbe0baf05','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:38.589907');
INSERT INTO "django_session" VALUES('ff8be4820bc703a73c0dae4b6922c5da','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:41.635689');
INSERT INTO "django_session" VALUES('82fd9e3e56961fea82841a5e11523b6f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:44.798097');
INSERT INTO "django_session" VALUES('f2ef92bd2e9b7d2d5c3829b4f155d478','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:47.844227');
INSERT INTO "django_session" VALUES('419d2d32170eead7725edeeb0b1c7d08','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:50.890014');
INSERT INTO "django_session" VALUES('958f5579358221eebbe71f5963d3a862','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:53.933967');
INSERT INTO "django_session" VALUES('38cb3b780666d3138814bc8994770a86','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:57:56.997072');
INSERT INTO "django_session" VALUES('ded6859dd7c9ad2f152975d4db2686b6','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:00.054055');
INSERT INTO "django_session" VALUES('f0fa615dcfa981c263e306c8df5d72b2','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:03.097625');
INSERT INTO "django_session" VALUES('ad89dc2163d6bf4c976395d147e8bb89','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:06.145950');
INSERT INTO "django_session" VALUES('570e47066bdac9c35834e14b7bea40c0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:09.203090');
INSERT INTO "django_session" VALUES('0fedbb4d4f617a0d88da87ce8d6e0696','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:12.255239');
INSERT INTO "django_session" VALUES('a87eb9d559ffd292ea5c970bf5c7d34b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:15.306441');
INSERT INTO "django_session" VALUES('5bac6df05ba79a59d2574d68c90438c8','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:18.357373');
INSERT INTO "django_session" VALUES('624b69f0250ae3d15b40eda5a3beb10f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:24.441545');
INSERT INTO "django_session" VALUES('95185b0f12111bb82690f197f783c3d0','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:27.564953');
INSERT INTO "django_session" VALUES('8acb8c71f401a682943c6197b82e44ab','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:30.698238');
INSERT INTO "django_session" VALUES('d5e69fafa0ab68f1923d70c0c9826140','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:33.744587');
INSERT INTO "django_session" VALUES('9ed4a1a756245f9693b4ecebd47606fe','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:36.791820');
INSERT INTO "django_session" VALUES('c34672310c8dc07e02f8335213a34f52','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:39.842776');
INSERT INTO "django_session" VALUES('76ef936871a9f6776f396e845d6af997','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:42.880967');
INSERT INTO "django_session" VALUES('4a28149396fa55dcb70dcf72358b1d1c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:45.924583');
INSERT INTO "django_session" VALUES('c1bba64423da1eaa87c255a9c6179480','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:48.972127');
INSERT INTO "django_session" VALUES('4254b02bfe4bd72d4ca54015bf21fe70','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:52.017395');
INSERT INTO "django_session" VALUES('97353305c4d292ed861ea619a7faae35','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:55.061662');
INSERT INTO "django_session" VALUES('a197492419d40632d54adb3f08bde2fd','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:58:58.131305');
INSERT INTO "django_session" VALUES('06ba85b45e2bac13f322679761e86aef','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:01.221972');
INSERT INTO "django_session" VALUES('4262eb4a06d49ef0fa6eae34511fd05c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:04.547152');
INSERT INTO "django_session" VALUES('349d5eab7d3666942bea76ed3bc2de33','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:07.593301');
INSERT INTO "django_session" VALUES('ac0f2188595e2be07542406199083b06','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:10.681968');
INSERT INTO "django_session" VALUES('f24983ce6d4261ccdf779b156d2e65ac','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:13.729340');
INSERT INTO "django_session" VALUES('4b557dc6a6d70eeff24ec7a5424138a4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:16.778065');
INSERT INTO "django_session" VALUES('133971842d3810a2aad56e61236c8ac7','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:19.820851');
INSERT INTO "django_session" VALUES('1d244d17246dfb2d177d9bd1df07057f','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:22.866981');
INSERT INTO "django_session" VALUES('81f0b40b3d7a44b4062d39248f53015e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:26.036946');
INSERT INTO "django_session" VALUES('8419eb78210528a393c3a736f3afc876','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:29.089418');
INSERT INTO "django_session" VALUES('bc44fb213d50b97c0289ce93efd00e72','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:32.181157');
INSERT INTO "django_session" VALUES('eee5ed8509c95ffeecaecde6071c0e95','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:35.212461');
INSERT INTO "django_session" VALUES('7a335930df1b7364111b38dc1b25da15','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:38.256831');
INSERT INTO "django_session" VALUES('af912e9bba3e9a40b38a091979305306','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:41.288394');
INSERT INTO "django_session" VALUES('a7c12fe4d9d071050e6d63bf72d6915d','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:44.318041');
INSERT INTO "django_session" VALUES('4f7e379ac31137632f9cdeae18b2c346','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:47.365668');
INSERT INTO "django_session" VALUES('af7c02c74a572691045cc50b49895d1c','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:50.412075');
INSERT INTO "django_session" VALUES('117bb134bca3f511e2382777895a07b8','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:53.461746');
INSERT INTO "django_session" VALUES('597074726481812eb56607bf20e20734','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:56.504590');
INSERT INTO "django_session" VALUES('a5253d989629e9f42568c417fd10846b','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 19:59:59.554286');
INSERT INTO "django_session" VALUES('8cc0467da7df9faf1879e4f7b283cc73','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 20:00:02.620987');
INSERT INTO "django_session" VALUES('7c95f6ffcbfbe346e5acefcd42099553','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 20:00:05.671968');
INSERT INTO "django_session" VALUES('88b14d10713056fa1ff6703ac0574873','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 20:00:08.714914');
INSERT INTO "django_session" VALUES('2e56929770b70ea3444b14e81d5e0be4','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 20:00:11.749076');
INSERT INTO "django_session" VALUES('3f73aefc5b3bd8fb5366e36204c777e9','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 20:00:14.792446');
INSERT INTO "django_session" VALUES('af98302c8a6849ed6ee39e13f498f469','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 20:00:17.838870');
INSERT INTO "django_session" VALUES('09e528078980d772603041de1dd9368a','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 20:00:20.880287');
INSERT INTO "django_session" VALUES('7d4d587e533bd1c17b477340da66af58','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 20:00:23.926484');
INSERT INTO "django_session" VALUES('3441f35260e1803e8ba2f7efa4e667ca','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 20:00:26.974523');
INSERT INTO "django_session" VALUES('ab0115ec987718e5f436faca50377f0e','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 20:00:30.019651');
INSERT INTO "django_session" VALUES('9ae63266a4348403053b723450523b0d','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-27 20:00:32.304895');
INSERT INTO "django_session" VALUES('76999f2c64514b421a82426b8ef222c5','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 20:15:00.101800');
INSERT INTO "django_session" VALUES('99f34ab6a3e44de7b7bfff7c9b063e73','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-27 20:42:07.692399');
INSERT INTO "django_session" VALUES('5e50c20bb51f3b7665b2aee21d2bd212','gAJ9cQEoVRh3YWl0X3VuaWRlbnRpZmllZF9wZXJzb25xAolVEl9hdXRoX3VzZXJfYmFja2VuZHED
VSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEEVQ1fYXV0aF91c2Vy
X2lkcQVLAVUTbGFzdF9qb3VybmFsX3VwZGF0ZXEGY2RhdGV0aW1lCmRhdGV0aW1lCnEHVQoH2gsP
DB00BptXhVJxCHUuODU5Yjg4ZTE4YmVkMjIyMDk2OTJlNGI5ZjA0MDE4OTc=
','2010-11-29 16:44:24.572769');
INSERT INTO "django_session" VALUES('11e90fdc95e25ed03b3474aace1da447','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-27 20:52:01.426311');
INSERT INTO "django_session" VALUES('5029dbe7a9e48bdbd3aa405a1331dd18','gAJ9cQEoVRh3YWl0X3VuaWRlbnRpZmllZF9wZXJzb25xAolVEl9hdXRoX3VzZXJfYmFja2VuZHED
VSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEEVQ1fYXV0aF91c2Vy
X2lkcQVLAVUTbGFzdF9qb3VybmFsX3VwZGF0ZXEGY2RhdGV0aW1lCmRhdGV0aW1lCnEHVQoH2gsN
FgsIAPjThVJxCHUuNWQ5NjEzNmM5YmZiNmYzYWRlOWVhZjc3NjgwYTBlY2U=
','2010-11-27 22:16:59.833306');
INSERT INTO "django_session" VALUES('7fae9030bec2337d4f84a2388587f306','gAJ9cQEoVRh3YWl0X3VuaWRlbnRpZmllZF9wZXJzb25xAolVDV9hdXRoX3VzZXJfaWRxA0sBVRJf
YXV0aF91c2VyX2JhY2tlbmRxBFUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJh
Y2tlbmRxBVUTbGFzdF9qb3VybmFsX3VwZGF0ZXEGY2RhdGV0aW1lCmRhdGV0aW1lCnEHVQoH2gsP
ERYYCo+rhVJxCHUuM2EyN2ZhMjY0Yzc0MGZkMDc0YzE4ZTQ3Mjg2Nzg5MzE=
','2010-11-29 19:02:30.384664');
INSERT INTO "django_session" VALUES('fbe1532a8496f45013c43012ed6f03f1','gAJ9cQEuYzg3MjE2MzczMDhiZTk2YThjMDA0NzNmY2UwZjkxNTg=
','2010-11-29 13:40:38.934864');
INSERT INTO "django_session" VALUES('895bed7135121291e805163e52ffad3a','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-29 13:56:14.594305');
INSERT INTO "django_session" VALUES('02c5c1e09bdf9bc5ea0271ca66beaec2','gAJ9cQEoVRh3YWl0X3VuaWRlbnRpZmllZF9wZXJzb25xAmNkYXRldGltZQpkYXRldGltZQpxA1UK
B9oLEAsmHgCgs4VScQRVEl9hdXRoX3VzZXJfYmFja2VuZHEFVSlkamFuZ28uY29udHJpYi5hdXRo
LmJhY2tlbmRzLk1vZGVsQmFja2VuZHEGVQ1fYXV0aF91c2VyX2lkcQdLAVUTbGFzdF9qb3VybmFs
X3VwZGF0ZXEIaANVCgfaCw8TJRoFuzOFUnEJdS5jYmNhOGI0YTJkNzM4YTU5MTdkMGE3ZDdjNWEz
OWJjOA==
','2010-11-30 11:38:28.768026');
INSERT INTO "django_session" VALUES('23c91e914c3b6cdc840d07eea062e1de','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-29 16:09:53.779265');
INSERT INTO "django_session" VALUES('75444214be030cdf74c1e39f6ded9d74','gAJ9cQEoVRh3YWl0X3VuaWRlbnRpZmllZF9wZXJzb25xAmNkYXRldGltZQpkYXRldGltZQpxA1UK
B9oLEAsmHgCgs4VScQRVEl9hdXRoX3VzZXJfYmFja2VuZHEFVSlkamFuZ28uY29udHJpYi5hdXRo
LmJhY2tlbmRzLk1vZGVsQmFja2VuZHEGVQ1fYXV0aF91c2VyX2lkcQdLAVUTbGFzdF9qb3VybmFs
X3VwZGF0ZXEIaANVCgfaCw8TJRoIXwKFUnEJdS45MDRjYjQzODM2Yzg3ZDhiYmQzMzI2NmMxMjEx
ZDgxMw==
','2010-11-30 11:38:30.067308');
INSERT INTO "django_session" VALUES('fe131c1ea99ea5a7ac8b282a7b478ccd','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-29 18:21:08.752021');
INSERT INTO "django_session" VALUES('58ff0976b4ba530ed6e1bf988627d4d5','gAJ9cQEoVRh3YWl0X3VuaWRlbnRpZmllZF9wZXJzb25xAolVDV9hdXRoX3VzZXJfaWRxA0sBVRJf
YXV0aF91c2VyX2JhY2tlbmRxBFUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJh
Y2tlbmRxBVUTbGFzdF9qb3VybmFsX3VwZGF0ZXEGY2RhdGV0aW1lCmRhdGV0aW1lCnEHVQoH2gsP
EyEeCvcUhVJxCHUuOTBkMzJhNGIzMzhlMTA0NjQ0MzEzMDgwYTZlODhjODc=
','2010-11-29 19:37:05.059421');
INSERT INTO "django_session" VALUES('38399f100f5ea795e5a69cba83b1b565','gAJ9cQEoVRh3YWl0X3VuaWRlbnRpZmllZF9wZXJzb25xAolVEl9hdXRoX3VzZXJfYmFja2VuZHED
VSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEEVQ1fYXV0aF91c2Vy
X2lkcQVLAVUTbGFzdF9qb3VybmFsX3VwZGF0ZXEGY2RhdGV0aW1lCmRhdGV0aW1lCnEHVQoH2gsP
Ey4nBX+OhVJxCHUuZjc2Y2MzODUwODk2NDkxODJkOTA2Nzk5ZmQ5MmY3OWU=
','2010-11-29 19:46:42.469571');
INSERT INTO "django_session" VALUES('68c99f0ad543b3e84d39f79f618ee4de','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-29 19:49:22.996968');
INSERT INTO "django_session" VALUES('1448fd11565513d703d8d528c63c437b','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjQ5NjM2ZDdjZmNjOGRlMGU4ZjNh
NGE0NzllYTQ4ZmQ5
','2010-11-29 19:53:24.990157');
CREATE TABLE "django_site" (
    "id" integer NOT NULL PRIMARY KEY,
    "domain" varchar(100) NOT NULL,
    "name" varchar(50) NOT NULL
);
INSERT INTO "django_site" VALUES(1,'example.com','example.com');
CREATE TABLE "videoclient_language" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(8) NOT NULL UNIQUE,
    "title" varchar(32) NOT NULL UNIQUE
);
INSERT INTO "videoclient_language" VALUES(1,'ru','Russian');
INSERT INTO "videoclient_language" VALUES(2,'en','English');
CREATE TABLE "videoclient_group" (
    "id" integer NOT NULL PRIMARY KEY,
    "title" varchar(32) NOT NULL UNIQUE
);
INSERT INTO "videoclient_group" VALUES(1,'help');
INSERT INTO "videoclient_group" VALUES(2,'trans');
CREATE TABLE "videoclient_translation" (
    "id" integer NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL REFERENCES "videoclient_group" ("id"),
    "phrase" varchar(4096) NOT NULL,
    "language_id" integer NOT NULL REFERENCES "videoclient_language" ("id"),
    "translate" varchar(4096) NOT NULL,
    "active" bool NOT NULL
);
INSERT INTO "videoclient_translation" VALUES(1,2,'Настройки камер',2,'Camera settings',1);
INSERT INTO "videoclient_translation" VALUES(2,2,'Выбор языка',2,'Select language',1);
INSERT INTO "videoclient_translation" VALUES(3,2,'Выход',2,'Exit',1);
INSERT INTO "videoclient_translation" VALUES(4,2,'Идентификация',2,'Identification',1);
INSERT INTO "videoclient_translation" VALUES(5,2,'Персоны',2,'Persons',1);
INSERT INTO "videoclient_translation" VALUES(6,2,'Обучение',2,'Training',1);
INSERT INTO "videoclient_translation" VALUES(7,2,'Настройки',2,'Settings',1);
INSERT INTO "videoclient_translation" VALUES(8,2,'Помощь',2,'Help',1);
INSERT INTO "videoclient_translation" VALUES(9,1,'Главная страница помощи',2,'Main page of help',1);
INSERT INTO "videoclient_translation" VALUES(10,1,'Персоны',2,'Persons',1);
INSERT INTO "videoclient_translation" VALUES(11,2,'Всего персон в базе',2,'Total number of persons in database',1);
INSERT INTO "videoclient_translation" VALUES(12,2,'Выбрать всё на странице',2,'Select all on page',1);
INSERT INTO "videoclient_translation" VALUES(13,2,'Удалить выделенные',2,'Remove selected',1);
INSERT INTO "videoclient_translation" VALUES(14,2,'Обнулить базу',2,'Reset database',1);
INSERT INTO "videoclient_translation" VALUES(15,2,'Имя',2,'Name',1);
INSERT INTO "videoclient_translation" VALUES(16,2,'Всего фотографий',2,'Total photos',1);
INSERT INTO "videoclient_translation" VALUES(17,2,'Все фотографии',2,'All photos',1);
INSERT INTO "videoclient_translation" VALUES(18,1,'Персоны',1,'',0);
INSERT INTO "videoclient_translation" VALUES(19,1,'Персона',1,'',0);
INSERT INTO "videoclient_translation" VALUES(20,2,'Обучение базы персон',2,'Training database of persons',1);
INSERT INTO "videoclient_translation" VALUES(21,2,'Вы можете загрузить',2,'You can download',1);
INSERT INTO "videoclient_translation" VALUES(22,2,'файлы форматов',2,'format image',1);
INSERT INTO "videoclient_translation" VALUES(23,2,'видео формата',2,'format video',1);
INSERT INTO "videoclient_translation" VALUES(24,2,'Обучить новой персоной',2,'Traning a new person',1);
INSERT INTO "videoclient_translation" VALUES(25,2,'Введите имя персоны',2,'Enter the name of the person',1);
INSERT INTO "videoclient_translation" VALUES(26,2,'Выберите персону',2,'Select a person',1);
INSERT INTO "videoclient_translation" VALUES(27,2,'Обучить с камеры',2,'Train with the camera',1);
INSERT INTO "videoclient_translation" VALUES(28,2,'Загрузить файлы',2,'Upload Files',1);
INSERT INTO "videoclient_translation" VALUES(29,2,'Назад',2,'Back',1);
INSERT INTO "videoclient_translation" VALUES(30,2,'Загрузите файлы',2,'Please upload files',1);
INSERT INTO "videoclient_translation" VALUES(31,2,'Выбрать персону из базы',2,'Choose a person from the database',1);
INSERT INTO "videoclient_translation" VALUES(32,1,'Обучение базы персон',2,'Training database of persons',1);
INSERT INTO "videoclient_translation" VALUES(33,1,'Обучение базы персон',1,'',0);
INSERT INTO "videoclient_translation" VALUES(34,2,'Настройки распознавания',2,'Recognition settings',1);
INSERT INTO "videoclient_translation" VALUES(35,1,'Главная страница помощи',1,'',0);
INSERT INTO "videoclient_translation" VALUES(36,2,'Закрыть окно',2,'Close the window',1);
INSERT INTO "videoclient_translation" VALUES(37,2,'Удаление',2,'Removing',1);
INSERT INTO "videoclient_translation" VALUES(38,2,'Далее',2,'Next',1);
INSERT INTO "videoclient_translation" VALUES(39,2,'Предупреждение',2,'Warning',1);
INSERT INTO "videoclient_translation" VALUES(40,2,'Обнуление базы',2,'Resetting the base',1);
INSERT INTO "videoclient_translation" VALUES(41,2,'Контакты',2,'Contacts',1);
INSERT INTO "videoclient_translation" VALUES(42,2,'информация',2,'Information',1);
INSERT INTO "videoclient_translation" VALUES(43,2,'техподдержка',2,'Support',1);
INSERT INTO "videoclient_translation" VALUES(44,2,'Простые решения',2,'Simple solutions',1);
INSERT INTO "videoclient_translation" VALUES(45,2,'Все права защищены',2,'All rights reserved',1);
INSERT INTO "videoclient_translation" VALUES(46,1,'Идентификация',1,'',0);
INSERT INTO "videoclient_translation" VALUES(47,1,'Идентификация',2,'Identification',1);
INSERT INTO "videoclient_translation" VALUES(48,1,'Помощь',2,'Help',1);
INSERT INTO "videoclient_translation" VALUES(49,2,'Настройки камеры',2,'The camera settings',1);
INSERT INTO "videoclient_translation" VALUES(50,2,'Настройка сервера',2,'Server configuration',1);
INSERT INTO "videoclient_translation" VALUES(51,2,'Настройка камеры',2,'Setting the camera',1);
INSERT INTO "videoclient_translation" VALUES(52,2,'Коммуникатор',2,'Communicator',1);
INSERT INTO "videoclient_translation" VALUES(53,2,'Изображение',2,'Image',1);
INSERT INTO "videoclient_translation" VALUES(54,2,'Яркость',2,'Brightness',1);
INSERT INTO "videoclient_translation" VALUES(55,2,'Применить',2,'Apply',1);
INSERT INTO "videoclient_translation" VALUES(56,2,'Резкость',2,'Harshness',1);
INSERT INTO "videoclient_translation" VALUES(57,2,'Насыщенность',2,'Saturation',1);
INSERT INTO "videoclient_translation" VALUES(58,2,'Контраст',2,'Contrast',1);
INSERT INTO "videoclient_translation" VALUES(59,2,'Качество',2,'Quality',1);
INSERT INTO "videoclient_translation" VALUES(60,2,'Режим освещения',2,'Mode lighting',1);
INSERT INTO "videoclient_translation" VALUES(61,2,'Автоматический',2,'Auto',1);
INSERT INTO "videoclient_translation" VALUES(62,2,'Внутри помещения',2,'Indoors',1);
INSERT INTO "videoclient_translation" VALUES(63,2,'Снаружи помещения',2,'Outdoors',1);
INSERT INTO "videoclient_translation" VALUES(64,2,'Смешанный',2,'Mixed',1);
INSERT INTO "videoclient_translation" VALUES(65,2,'Режим низкой освещённости',2,'Low light Mode',1);
INSERT INTO "videoclient_translation" VALUES(66,2,'Время экспозиции',2,'Exposure time',1);
INSERT INTO "videoclient_translation" VALUES(67,2,'Быстро',2,'Quickly',1);
INSERT INTO "videoclient_translation" VALUES(68,2,'Сбалансировано',2,'Balanced',1);
INSERT INTO "videoclient_translation" VALUES(69,2,'Качественно',2,'Qualitatively',1);
INSERT INTO "videoclient_translation" VALUES(70,2,'Moon Light (TM)',2,'',0);
INSERT INTO "videoclient_translation" VALUES(71,2,'Частота',2,'Frequency',1);
INSERT INTO "videoclient_translation" VALUES(72,2,'День',2,'Day',1);
INSERT INTO "videoclient_translation" VALUES(73,2,'Ночь',2,'Night',1);
INSERT INTO "videoclient_translation" VALUES(74,2,'Дневной режим',2,'Day mode',1);
INSERT INTO "videoclient_translation" VALUES(75,2,'Ночной режим',2,'Night mode',1);
INSERT INTO "videoclient_translation" VALUES(76,2,'Разрешение камеры и область захвата',2,'Resolution of the camera and capture area',1);
INSERT INTO "videoclient_translation" VALUES(77,2,'Разрешение камеры',2,'Camera resolution',1);
INSERT INTO "videoclient_translation" VALUES(78,2,'Область захвата',2,'Capture area',1);
INSERT INTO "videoclient_translation" VALUES(79,2,'Дисторсия',2,'Distortion',1);
INSERT INTO "videoclient_translation" VALUES(80,2,'Выпуклость',2,'Bulge',1);
INSERT INTO "videoclient_translation" VALUES(81,2,'Интенсивность',2,'Intensity',1);
INSERT INTO "videoclient_translation" VALUES(82,2,'Смещение по',2,'Offset',1);
INSERT INTO "videoclient_translation" VALUES(83,2,'Количество кадров',2,'Number of frames',1);
INSERT INTO "videoclient_translation" VALUES(84,1,'Настройки камер',1,'',0);
INSERT INTO "videoclient_translation" VALUES(85,1,'Настройки камер',2,'Camera settings',1);
INSERT INTO "videoclient_translation" VALUES(86,2,'Расстояние между глаз',2,'The distance between the eyes',1);
INSERT INTO "videoclient_translation" VALUES(87,1,'Настройки распознавания',2,'Recognition settings',1);
INSERT INTO "videoclient_translation" VALUES(88,2,'Сохранить профиль',2,'Save settings',1);
INSERT INTO "videoclient_translation" VALUES(89,2,'Для сохранения настроек для всех камер выбранного коммуникатора',2,'To save your settings for all cameras selected device',1);
INSERT INTO "videoclient_translation" VALUES(90,2,'Загрузить настройки',2,'Load settings',1);
INSERT INTO "videoclient_translation" VALUES(91,2,'Для загрузки сохранённых настроек для всех камер выбранного коммуникатора',2,'To load the saved settings for all cameras selected device',1);
INSERT INTO "videoclient_translation" VALUES(92,2,'Выберите коммуникатор',2,'Select device',1);
INSERT INTO "videoclient_translation" VALUES(93,2,'Список камер',2,'List chambers',1);
INSERT INTO "videoclient_translation" VALUES(94,2,'Режим сервера',2,'Server mode',1);
INSERT INTO "videoclient_translation" VALUES(95,2,'Название камеры',2,'Camera title',1);
INSERT INTO "videoclient_translation" VALUES(96,2,'Видео режим',2,'Video',1);
INSERT INTO "videoclient_translation" VALUES(97,2,'Детект. лиц',2,'Face detect',1);
INSERT INTO "videoclient_translation" VALUES(98,2,'Идент. лиц',2,'Face ident.',1);
INSERT INTO "videoclient_translation" VALUES(99,2,'Камера выкл.',2,'Camera off',1);
INSERT INTO "videoclient_translation" VALUES(100,2,'Обновление списка камер',2,'Updating list of cameras',1);
INSERT INTO "videoclient_translation" VALUES(101,2,'Введите максимальное количество камер, которое должен найти коммуникатор',2,'Enter the maximum number of cameras, which must find a communicator',1);
INSERT INTO "videoclient_translation" VALUES(102,1,'Помощь',1,'',0);
INSERT INTO "videoclient_translation" VALUES(103,2,'Ошибка подключения!',2,'Connection error!',1);
INSERT INTO "videoclient_translation" VALUES(104,2,'недоступен',2,'unavailable',1);
INSERT INTO "videoclient_translation" VALUES(105,2,'Пожалуйста, попробуйте подключиться позднее',2,'Please try connecting again later',1);
INSERT INTO "videoclient_translation" VALUES(106,1,'Настройки распознавания',1,'',0);
INSERT INTO "videoclient_translation" VALUES(107,1,'Настройки камеры',1,'',0);
INSERT INTO "videoclient_translation" VALUES(108,2,'Параметр не применился. Пожалуйста, попробуйте ещё раз',2,'Parameter does not apply. Please try again',1);
INSERT INTO "videoclient_translation" VALUES(109,2,'Выберите, пожалуйста, хотя бы одну персону',2,'Please select at least one person',1);
INSERT INTO "videoclient_translation" VALUES(110,2,'Выберите, пожалуйста, хотя бы одну фотографию персоны',2,'Please select at least one photograph of the person',1);
INSERT INTO "videoclient_translation" VALUES(111,2,'Вы, действительно, хотите удалить выбранных персон',2,'Want you delete the selected persons',1);
INSERT INTO "videoclient_translation" VALUES(112,2,'шт',2,'pcs',1);
INSERT INTO "videoclient_translation" VALUES(113,2,'Вы, действительно, хотите удалить выбранные фотографии',2,'Want you delete the selected photos',1);
INSERT INTO "videoclient_translation" VALUES(114,2,'Вы, действительно, хотите удалить базу персон',2,'Want you delete the database of persons',1);
INSERT INTO "videoclient_translation" VALUES(115,2,'Выберите, пожалуйста, хотя бы одно изображение',2,'Please select at least one image',1);
INSERT INTO "videoclient_translation" VALUES(116,2,'Значение должно содержать только цифры',2,'The value must contain only numbers',1);
INSERT INTO "videoclient_translation" VALUES(117,2,'Введена слишком большая ширина для области захвата',2,'Put too much width to the capture region',1);
INSERT INTO "videoclient_translation" VALUES(118,2,'Введено слишком большое смещение по координате',2,'Introduced too much bias in the coordinate',1);
INSERT INTO "videoclient_translation" VALUES(119,2,'Введена слишком большая высота для области захвата',2,'Put too great a height for the capture region',1);
INSERT INTO "videoclient_translation" VALUES(126,2,'Введено слишком большое значение',2,'Introduced too much',1);
INSERT INTO "videoclient_translation" VALUES(127,2,'Введите имя персоны, пожалуйста',2,'Enter the name of the person, please',1);
INSERT INTO "videoclient_translation" VALUES(128,2,'Выберите персону из базы, пожалуйста',2,'Select a person from the database, please',1);
INSERT INTO "videoclient_translation" VALUES(129,2,'Обучение персоны',2,'Training person',1);
INSERT INTO "videoclient_translation" VALUES(130,2,'Обучение новой персоной',2,'Training of new person',1);
INSERT INTO "videoclient_translation" VALUES(131,2,'Камера недоступна',2,'Camera is unavailable',1);
INSERT INTO "videoclient_translation" VALUES(132,2,'Вход в систему',2,'Login',1);
INSERT INTO "videoclient_translation" VALUES(133,2,'Система администрирования',2,'System administration',1);
INSERT INTO "videoclient_translation" VALUES(134,2,'Логин',2,'User',1);
INSERT INTO "videoclient_translation" VALUES(135,2,'Пароль',2,'Password',1);
INSERT INTO "videoclient_translation" VALUES(136,2,'Войти',2,'Enter',1);
INSERT INTO "videoclient_translation" VALUES(137,2,'Введено слишком большое значение для параметра "Яркость"',2,'Introduced too great a value for the "Value"',1);
INSERT INTO "videoclient_translation" VALUES(138,2,'Введено слишком большое значение для параметра "Резкость"',2,'Introduced too great a value for "Sharpness"',1);
INSERT INTO "videoclient_translation" VALUES(139,2,'Введено слишком большое значение для параметра "Насыщенность"',2,'Introduced too great a value for the "Saturation"',1);
INSERT INTO "videoclient_translation" VALUES(140,2,'Введено слишком большое значение для параметра "Контраст"',2,'Introduced too great a value for "Contrast"',1);
INSERT INTO "videoclient_translation" VALUES(141,2,'Введено слишком большое значение для параметра "Качество"',2,'Introduced too great a value for "Quality"',1);
INSERT INTO "videoclient_translation" VALUES(142,2,'Введённое значение для параметра "Время экспозиции" находится вне указанного диапазона',2,'Introduced a value for exposure time "is outside the specified range',1);
INSERT INTO "videoclient_translation" VALUES(143,1,'Настройки камеры',2,'The camera settings',1);
INSERT INTO "videoclient_translation" VALUES(144,2,'Время экспозиции (мс)',2,'Exposure time (ms)',1);
INSERT INTO "videoclient_translation" VALUES(145,2,'Задержка видео для обработки (мс)',2,'Video processing delay (ms)',1);
INSERT INTO "videoclient_translation" VALUES(146,2,'Макс кол-во обрабатываемых кадров',2,'Max number of processed frames',1);
INSERT INTO "videoclient_translation" VALUES(150,2,'Максимальное количество одновременно обрабатываемых кадров',2,'Maximum number of concurrently processed frames',1);
INSERT INTO "videoclient_translation" VALUES(151,2,'При детектировании',2,'In the face identification',1);
INSERT INTO "videoclient_translation" VALUES(152,2,'При идентификации',2,'In the face recognition',1);
INSERT INTO "videoclient_translation" VALUES(153,2,'При обучении',2,'In the training',1);
INSERT INTO "videoclient_translation" VALUES(154,2,'Камера выключена',2,'Camera is switched off',1);
INSERT INTO "videoclient_translation" VALUES(155,2,'при детектировании',2,'in the detection',1);
INSERT INTO "videoclient_translation" VALUES(156,2,'при идентификации',2,'in the identification',1);
INSERT INTO "videoclient_translation" VALUES(157,2,'при обучении',2,'in the training',1);
INSERT INTO "videoclient_translation" VALUES(158,2,'Персона',2,'Person',1);
INSERT INTO "videoclient_translation" VALUES(159,1,'Персона',2,'Person',1);
INSERT INTO "videoclient_translation" VALUES(160,2,'Всего фотографий выбранной персоны',2,'Total pictures in the selected person',1);
INSERT INTO "videoclient_translation" VALUES(161,2,'Найти камеры',2,'Find camera',1);
INSERT INTO "videoclient_translation" VALUES(162,2,'Обновить список камер для данного коммуникатора',2,'Update the list of cameras for this device',1);
INSERT INTO "videoclient_translation" VALUES(163,2,'Добавить',2,'Add',1);
INSERT INTO "videoclient_translation" VALUES(164,2,'Добавить камеру вручную',2,'Add the camera manually',1);
INSERT INTO "videoclient_translation" VALUES(165,2,'Добавление камеры вручную',2,'Adding a camera manual',1);
INSERT INTO "videoclient_translation" VALUES(166,2,'Модель камеры',2,'Camera model',1);
INSERT INTO "videoclient_translation" VALUES(167,2,'адрес',2,'address',1);
INSERT INTO "videoclient_translation" VALUES(168,2,'Порт',2,'Port',1);
INSERT INTO "videoclient_translation" VALUES(169,2,'Номер камеры',2,'Camera number',1);
INSERT INTO "videoclient_translation" VALUES(170,2,'Пользователь',2,'User',1);
INSERT INTO "videoclient_translation" VALUES(171,2,'Подключиться',2,'Connect',1);
INSERT INTO "videoclient_translation" VALUES(172,2,'Первая страница',2,'First page',1);
INSERT INTO "videoclient_translation" VALUES(173,2,'Начало',2,'Home',1);
INSERT INTO "videoclient_translation" VALUES(174,2,'Последняя страница',2,'Last Page',1);
INSERT INTO "videoclient_translation" VALUES(175,2,'Конец',2,'End',1);
INSERT INTO "videoclient_translation" VALUES(176,2,'Предыдущая страница',2,'Previous page',1);
INSERT INTO "videoclient_translation" VALUES(177,2,'Следующая страница',2,'Next page',1);
INSERT INTO "videoclient_translation" VALUES(178,2,'Вперёд',2,'Next',1);
INSERT INTO "videoclient_translation" VALUES(179,2,'Камера не добавилась. Пожалуйста, попробуйте ещё раз',2,'The camera is not added. Please try again',1);
INSERT INTO "videoclient_translation" VALUES(180,2,'Камера не добавлена. Пожалуйста, попробуйте ещё раз',2,'The camera is not added. Please try again',1);
INSERT INTO "videoclient_translation" VALUES(181,2,'Камера успешно добавлена.',2,'The camera was successfully added.',1);
INSERT INTO "videoclient_translation" VALUES(182,2,'Персон с именем',2,'Persons with the name',1);
INSERT INTO "videoclient_translation" VALUES(183,2,'в базе не найдено',2,'in the database is not found',1);
INSERT INTO "videoclient_translation" VALUES(184,2,'Создать персону',2,'Create a person',1);
INSERT INTO "videoclient_translation" VALUES(185,2,'Найти персону',2,'Find person',1);
INSERT INTO "videoclient_translation" VALUES(186,2,'Просмотр видео',2,'View',1);
INSERT INTO "videoclient_translation" VALUES(187,2,'Настроить',2,'Customize',1);
INSERT INTO "videoclient_translation" VALUES(188,2,'Минимальный размер лица',2,'Min face width',1);
INSERT INTO "videoclient_translation" VALUES(189,2,'Настройка сервера ',2,'Server settings',1);
INSERT INTO "videoclient_translation" VALUES(190,2,'Настройка дисторсии',2,'Settings distortion',1);
INSERT INTO "videoclient_translation" VALUES(191,1,'Настройки дисторсии',2,'Settings distortion',1);
INSERT INTO "videoclient_translation" VALUES(192,1,'Настройки дисторсии',1,'',0);
INSERT INTO "videoclient_translation" VALUES(193,2,'Настройки дисторсии',2,'Settings distortion',1);
INSERT INTO "videoclient_translation" VALUES(194,2,'Выбор камеры',2,'Choose camera',1);
INSERT INTO "videoclient_translation" VALUES(195,1,'Выбор камеры для обучения',2,'Choose camera for training',1);
INSERT INTO "videoclient_translation" VALUES(196,2,'Выбор',2,'Choose',1);
INSERT INTO "videoclient_translation" VALUES(197,1,'Выбор камеры для обучения',1,'',0);
INSERT INTO "videoclient_translation" VALUES(198,2,'Обучение с камеры',2,'Training from the camera',1);
INSERT INTO "videoclient_translation" VALUES(199,2,'Ошибка подключения! Камера с таким названием недоступна. Пожалуйста, попробуйте подключиться позднее',2,'Connection Error! Camera with such a title is not available. Please try connecting again later',1);
INSERT INTO "videoclient_translation" VALUES(200,2,'Пожалуйста, подождите',2,'Please wait',1);
INSERT INTO "videoclient_translation" VALUES(201,2,'Камера не выбрана',2,'The camera is not selected',1);
INSERT INTO "videoclient_translation" VALUES(202,2,'Версия',2,'Version',1);
INSERT INTO "videoclient_translation" VALUES(203,2,'Продукты',2,'',0);
INSERT INTO "videoclient_translation" VALUES(204,2,'Пользователи',2,'',0);
INSERT INTO "videoclient_translation" VALUES(205,2,'Журнал',2,'',0);
INSERT INTO "videoclient_translation" VALUES(206,2,'Сигнал',2,'',0);
INSERT INTO "videoclient_translation" VALUES(207,2,'Запись',2,'',0);
INSERT INTO "videoclient_translation" VALUES(208,2,'КПП',2,'',0);
INSERT INTO "videoclient_translation" VALUES(209,2,'Введите имя пользователя',2,'',0);
INSERT INTO "videoclient_translation" VALUES(210,2,'Найти пользователя',2,'',0);
INSERT INTO "videoclient_translation" VALUES(211,2,'Всего пользователей в базе',2,'',0);
INSERT INTO "videoclient_translation" VALUES(212,2,'Анкета пользователя:',2,'',0);
INSERT INTO "videoclient_translation" VALUES(213,2,'Сигналы',2,'',0);
INSERT INTO "videoclient_translation" VALUES(214,2,'Розыск',2,'',0);
INSERT INTO "videoclient_translation" VALUES(215,1,'Просмотр',1,'',0);
CREATE TABLE "django_admin_log" (
    "id" integer NOT NULL PRIMARY KEY,
    "action_time" datetime NOT NULL,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "content_type_id" integer REFERENCES "django_content_type" ("id"),
    "object_id" text,
    "object_repr" varchar(200) NOT NULL,
    "action_flag" smallint unsigned NOT NULL,
    "change_message" text NOT NULL
);
INSERT INTO "django_admin_log" VALUES(1,'2010-10-15 13:13:08.443966',1,8,'1','ru:Russian',1,'');
INSERT INTO "django_admin_log" VALUES(2,'2010-10-15 13:13:18.174008',1,8,'2','en:English',1,'');
INSERT INTO "django_admin_log" VALUES(3,'2010-10-15 13:13:28.905996',1,9,'1','help',1,'');
INSERT INTO "django_admin_log" VALUES(4,'2010-10-15 13:13:37.293442',1,9,'2','trans',1,'');
INSERT INTO "django_admin_log" VALUES(5,'2010-10-19 07:36:15.287935',1,10,'8','V trans:Помощь -en:English-> Help',2,'Изменен translate и active.');
INSERT INTO "django_admin_log" VALUES(6,'2010-10-19 07:42:22.050933',1,10,'3','V trans:Выход -en:English-> Exit',2,'Изменен translate и active.');
INSERT INTO "django_admin_log" VALUES(7,'2010-10-19 10:21:07.106730',1,10,'125','X trans:Введённое значение для параметра \"Время экспозиции\" находится вне указанного диапазона -en:English-> ',3,'');
INSERT INTO "django_admin_log" VALUES(8,'2010-10-19 10:21:07.156453',1,10,'124','X trans:Введено слишком большое значение для параметра \"Качество\" -en:English-> ',3,'');
INSERT INTO "django_admin_log" VALUES(9,'2010-10-19 10:21:07.161328',1,10,'123','X trans:Введено слишком большое значение для параметра \"Контраст\" -en:English-> ',3,'');
INSERT INTO "django_admin_log" VALUES(10,'2010-10-19 10:21:07.165277',1,10,'122','X trans:Введено слишком большое значение для параметра \"Насыщенность\" -en:English-> ',3,'');
INSERT INTO "django_admin_log" VALUES(11,'2010-10-19 10:21:07.169388',1,10,'121','X trans:Введено слишком большое значение для параметра \"Резкость\" -en:English-> ',3,'');
INSERT INTO "django_admin_log" VALUES(12,'2010-10-19 10:21:07.173208',1,10,'120','X trans:Введено слишком большое значение для параметра \"Яркость\" -en:English-> ',3,'');
INSERT INTO "django_admin_log" VALUES(13,'2010-10-19 12:01:20.907444',1,12,'1','192.168.0.55:12600',1,'');
INSERT INTO "django_admin_log" VALUES(14,'2010-10-19 12:08:14.897307',1,12,'2','192.168.0.55:13600',1,'');
INSERT INTO "django_admin_log" VALUES(15,'2010-10-19 12:13:40.498323',1,13,'1','192.168.0.55:16544 lLogin pPassword dima',1,'');
INSERT INTO "django_admin_log" VALUES(16,'2010-10-19 12:15:07.061192',1,13,'1','192.168.0.55:16544 lLogin pPassword dima_shilov',2,'Changed user.');
INSERT INTO "django_admin_log" VALUES(17,'2010-10-19 13:01:01.769478',1,10,'143','X trans:кспозиции" находится вне указанного диапазона -en:English-> ',3,'');
INSERT INTO "django_admin_log" VALUES(18,'2010-10-19 13:01:01.809578',1,10,'142','X trans:Введённое значение для параметра "Врем -en:English-> ',3,'');
INSERT INTO "django_admin_log" VALUES(19,'2010-10-19 13:03:36.321874',1,10,'149','X trans:при обучении -en:English-> ',3,'');
INSERT INTO "django_admin_log" VALUES(20,'2010-10-19 13:03:36.332014',1,10,'148','X trans:при идентификации -en:English-> ',3,'');
INSERT INTO "django_admin_log" VALUES(21,'2010-10-19 13:03:36.335575',1,10,'147','X trans:при детектировании -en:English-> ',3,'');
INSERT INTO "django_admin_log" VALUES(22,'2010-10-19 14:17:01.204405',1,12,'3','192.168.0.55:14600',1,'');
INSERT INTO "django_admin_log" VALUES(23,'2010-10-19 14:17:25.749620',1,12,'4','192.168.0.123:12600',1,'');
INSERT INTO "django_admin_log" VALUES(24,'2010-10-19 14:18:15.551156',1,12,'5','192.168.0.123:13600',1,'');
INSERT INTO "django_admin_log" VALUES(25,'2010-10-19 14:18:32.707088',1,12,'6','192.168.0.123:14600',1,'');
INSERT INTO "django_admin_log" VALUES(26,'2010-10-19 14:19:08.512975',1,12,'7','192.168.0.235:12600',1,'');
INSERT INTO "django_admin_log" VALUES(27,'2010-10-19 14:19:21.279231',1,12,'8','192.168.0.235:16544',1,'');
INSERT INTO "django_admin_log" VALUES(28,'2010-10-19 14:27:55.567785',1,13,'1','192.168.0.55:16544 lLogin pPassword communicator',2,'Changed user.');
INSERT INTO "django_admin_log" VALUES(29,'2010-10-19 14:33:59.693183',1,10,'7','V trans:Настройки -en:English-> Settings',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(30,'2010-10-19 14:34:20.876839',1,10,'1','V trans:Настройки камер -en:English-> Settings of cameras',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(31,'2010-10-19 14:34:44.335117',1,10,'34','V trans:Настройки распознавания -en:English-> Settings of recognition',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(32,'2010-10-19 14:35:04.265269',1,10,'49','V trans:Настройки камеры -en:English-> Settings of camera',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(33,'2010-10-19 14:35:27.492184',1,10,'158','V trans:Персона -en:English-> Person',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(34,'2010-10-19 14:35:58.543003',1,10,'5','V trans:Персоны -en:English-> Persons',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(35,'2010-10-19 14:37:13.977104',1,10,'4','V trans:Идентификация -en:English-> Identification',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(36,'2010-10-19 14:37:39.461025',1,10,'6','V trans:Обучение -en:English-> Learning',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(37,'2010-10-19 14:49:06.178730',1,10,'48','X help:Помощь -en:English-> Help',2,'Изменен translate.');
INSERT INTO "django_admin_log" VALUES(38,'2010-10-19 14:58:28.724811',1,12,'9','192.168.0.235:12600',1,'');
INSERT INTO "django_admin_log" VALUES(39,'2010-10-20 10:11:10.236131',1,10,'178','V trans:Вперёд -en:English-> Next',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(40,'2010-10-20 10:11:25.994434',1,10,'177','V trans:Следующая страница -en:English-> Next page',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(41,'2010-10-20 10:12:17.221442',1,10,'176','V trans:Предыдущая страница -en:English-> Previous page',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(42,'2010-10-20 10:13:08.027267',1,10,'175','V trans:Конец -en:English-> End',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(43,'2010-10-20 10:14:24.345831',1,10,'174','V trans:Последняя страница -en:English-> Last Page',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(44,'2010-10-20 10:14:54.530739',1,10,'173','V trans:Начало -en:English-> Home',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(45,'2010-10-20 10:15:12.726645',1,10,'172','V trans:Первая страница -en:English-> First page',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(46,'2010-10-20 10:15:33.422289',1,10,'171','V trans:Подключиться -en:English-> Connect',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(47,'2010-10-20 10:15:44.463505',1,10,'170','V trans:Пользователь -en:English-> User',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(48,'2010-10-20 10:16:39.389578',1,10,'169','V trans:Номер камеры -en:English-> Camera number',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(49,'2010-10-20 10:16:52.744116',1,10,'168','V trans:Порт -en:English-> Port',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(50,'2010-10-20 10:17:15.374319',1,10,'167','V trans:адрес -en:English-> address',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(51,'2010-10-20 10:17:37.148858',1,10,'166','V trans:Модель камеры -en:English-> Camera model',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(52,'2010-10-20 10:21:01.890103',1,10,'165','V trans:Добавление камеры вручную -en:English-> Add the camera manually',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(53,'2010-10-20 10:23:05.684675',1,10,'164','V trans:Добавить камеру вручную -en:English-> Add the camera manually',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(54,'2010-10-20 10:24:57.390624',1,10,'165','V trans:Добавление камеры вручную -en:English-> Adding a camera manual',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(55,'2010-10-20 10:27:12.311607',1,10,'163','V trans:Добавить -en:English-> Add',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(56,'2010-10-20 10:30:58.993475',1,10,'162','V trans:Обновить список камер для данного коммуникатора -en:English-> Update the list of cameras for this device',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(57,'2010-10-20 10:31:21.210875',1,10,'161','V trans:Найти камеры -en:English-> Find Camera',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(58,'2010-10-20 10:31:43.121506',1,10,'160','V trans:Всего фотографий выбранной персоны -en:English-> Total pictures in the selected person',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(59,'2010-10-20 10:32:07.410272',1,10,'134','V trans:Логин -en:English-> Login',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(60,'2010-10-20 10:32:25.741146',1,10,'136','V trans:Войти -en:English-> Enter',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(61,'2010-10-20 10:32:57.228981',1,10,'135','V trans:Пароль -en:English-> Password',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(62,'2010-10-20 10:33:35.916059',1,10,'133','X trans:Система администрирования -en:English-> System administration',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(63,'2010-10-20 10:33:43.794147',1,10,'133','V trans:Система администрирования -en:English-> System administration',2,'Changed active.');
INSERT INTO "django_admin_log" VALUES(64,'2010-10-20 10:34:09.111209',1,10,'132','V trans:Вход в систему -en:English-> Login',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(65,'2010-10-20 10:34:22.244763',1,10,'134','V trans:Логин -en:English-> User',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(66,'2010-10-20 10:35:15.687959',1,10,'41','V trans:Контакты -en:English-> Contacts',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(67,'2010-10-20 10:35:44.506970',1,10,'42','V trans:информация -en:English-> Information',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(68,'2010-10-20 10:36:30.444526',1,10,'43','V trans:техподдержка -en:English-> Support',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(69,'2010-10-20 10:37:00.920610',1,10,'45','V trans:Все права защищены -en:English-> All rights reserved',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(70,'2010-10-20 10:37:55.814395',1,10,'44','V trans:Простые решения -en:English-> Simple solutions',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(71,'2010-10-20 10:46:28.877323',1,10,'11','V trans:Всего персон в базе -en:English-> Total number of persons in database',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(72,'2010-10-20 10:46:56.725326',1,10,'12','V trans:Выбрать всё на странице -en:English-> Select all on page',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(73,'2010-10-20 10:47:43.020450',1,10,'25','V trans:Введите имя персоны -en:English-> Enter the name of the person',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(74,'2010-10-20 10:48:04.309008',1,10,'15','V trans:Имя -en:English-> Name',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(75,'2010-10-20 10:48:34.936461',1,10,'16','V trans:Всего фотографий -en:English-> Total photos',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(76,'2010-10-20 10:57:30.993236',1,10,'179','V trans:Камера не добавилась. Пожалуйста, попробуйте ещё раз -en:English-> The camera is not added. Please try again',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(77,'2010-10-20 10:57:52.333908',1,10,'181','V trans:Камера успешно добавлена. -en:English-> The camera was successfully added.',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(78,'2010-10-20 10:58:20.943041',1,10,'180','V trans:Камера не добавлена. Пожалуйста, попробуйте ещё раз -en:English-> The camera is not added. Please try again',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(79,'2010-10-20 11:04:08.591773',1,10,'17','V trans:Все фотографии -en:English-> All photos',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(80,'2010-10-20 11:05:19.821894',1,10,'13','V trans:Удалить выделенные -en:English-> Remove selected',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(81,'2010-10-20 11:06:01.988374',1,10,'14','V trans:Обнулить базу -en:English-> Reset database',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(82,'2010-10-20 11:16:16.274462',1,13,'1','192.168.0.235:16544 lLogin pPassword communicator',2,'Changed host.');
INSERT INTO "django_admin_log" VALUES(83,'2010-10-20 11:19:47.844582',1,12,'1','192.168.0.55:12600',2,'Changed active.');
INSERT INTO "django_admin_log" VALUES(84,'2010-10-20 11:19:51.859617',1,12,'2','192.168.0.55:13600',2,'Changed active.');
INSERT INTO "django_admin_log" VALUES(85,'2010-10-20 11:19:56.825598',1,12,'3','192.168.0.55:14600',2,'Changed active.');
INSERT INTO "django_admin_log" VALUES(86,'2010-10-20 11:20:02.496955',1,12,'4','192.168.0.123:12600',2,'Changed active.');
INSERT INTO "django_admin_log" VALUES(87,'2010-10-20 11:20:16.331573',1,12,'5','192.168.0.123:13600',2,'No fields changed.');
INSERT INTO "django_admin_log" VALUES(88,'2010-10-20 11:20:25.041921',1,12,'4','192.168.0.123:12600',2,'Changed active.');
INSERT INTO "django_admin_log" VALUES(89,'2010-10-20 11:20:30.336568',1,12,'3','192.168.0.55:14600',2,'Changed active.');
INSERT INTO "django_admin_log" VALUES(90,'2010-10-20 11:20:35.111942',1,12,'2','192.168.0.55:13600',2,'Changed active.');
INSERT INTO "django_admin_log" VALUES(91,'2010-10-20 11:20:41.484442',1,12,'1','192.168.0.55:12600',2,'Changed active.');
INSERT INTO "django_admin_log" VALUES(92,'2010-10-20 11:21:12.860749',1,13,'1','192.168.0.55:16544 lLogin pPassword communicator',2,'Changed host.');
INSERT INTO "django_admin_log" VALUES(93,'2010-10-20 12:10:18.135660',1,10,'183','V trans:в базе не найдено -en:English-> in the database is not found',2,'Изменен translate и active.');
INSERT INTO "django_admin_log" VALUES(94,'2010-10-20 12:11:09.756493',1,10,'182','V trans:Персон с именем -en:English-> Persons with the name',2,'Изменен translate и active.');
INSERT INTO "django_admin_log" VALUES(95,'2010-10-20 12:11:21.673226',1,10,'183','V trans:в базе не найдено -en:English-> in the database is not found',2,'Ни одно поле не изменено.');
INSERT INTO "django_admin_log" VALUES(96,'2010-10-20 12:12:30.836444',1,10,'150','V trans:Максимальное количество одновременно обрабатываемых кадров -en:English-> Maximum number of concurrently processed frames',2,'Изменен translate и active.');
INSERT INTO "django_admin_log" VALUES(97,'2010-10-20 12:14:59.049522',1,10,'157','V trans:при обучении -en:English-> in the training',2,'Изменен translate и active.');
INSERT INTO "django_admin_log" VALUES(98,'2010-10-20 12:15:15.391765',1,10,'153','V trans:При обучении -en:English-> In the training',2,'Изменен translate и active.');
INSERT INTO "django_admin_log" VALUES(99,'2010-10-20 12:15:57.919842',1,10,'156','V trans:при идентификации -en:English-> in the identification',2,'Изменен translate и active.');
INSERT INTO "django_admin_log" VALUES(100,'2010-10-20 12:16:12.875870',1,10,'152','V trans:При идентификации -en:English-> In the identification',2,'Изменен translate и active.');
INSERT INTO "django_admin_log" VALUES(101,'2010-10-20 12:17:06.738684',1,10,'155','V trans:при детектировании -en:English-> in the detection',2,'Изменен translate и active.');
INSERT INTO "django_admin_log" VALUES(102,'2010-10-20 12:17:21.121647',1,10,'151','V trans:При детектировании -en:English-> In the detection',2,'Изменен translate и active.');
INSERT INTO "django_admin_log" VALUES(103,'2010-10-20 12:18:22.672691',1,10,'154','V trans:Камера выключена -en:English-> Camera is switched off',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(104,'2010-10-20 12:18:59.531103',1,10,'146','V trans:Макс кол-во обрабатываемых кадров -en:English-> Max number of processed frames',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(105,'2010-10-20 12:19:41.841106',1,10,'145','V trans:Задержка видео для обработки (мс) -en:English-> Video processing delay (ms)',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(106,'2010-10-20 12:20:49.921101',1,10,'144','V trans:Время экспозиции (мс) -en:English-> Exposure time (ms)',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(107,'2010-10-20 12:21:25.386832',1,10,'142','V trans:Введённое значение для параметра "Время экспозиции" находится вне указанного диапазона -en:English-> Introduced a value for exposure time "is outside the specified range',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(108,'2010-10-20 12:21:50.807150',1,10,'141','V trans:Введено слишком большое значение для параметра "Качество" -en:English-> Introduced too great a value for "Quality"',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(109,'2010-10-20 12:22:17.531595',1,10,'140','V trans:Введено слишком большое значение для параметра "Контраст" -en:English-> Introduced too great a value for "Contrast"',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(110,'2010-10-20 12:22:45.872754',1,10,'139','X trans:Введено слишком большое значение для параметра "Насыщенность" -en:English-> Introduced too great a value for the "Saturation"',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(111,'2010-10-20 12:22:56.909286',1,10,'139','V trans:Введено слишком большое значение для параметра "Насыщенность" -en:English-> Introduced too great a value for the "Saturation"',2,'Changed active.');
INSERT INTO "django_admin_log" VALUES(112,'2010-10-20 12:23:26.562674',1,10,'138','V trans:Введено слишком большое значение для параметра "Резкость" -en:English-> Introduced too great a value for "Sharpness"',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(113,'2010-10-20 12:23:50.760777',1,10,'137','V trans:Введено слишком большое значение для параметра "Яркость" -en:English-> Introduced too great a value for the "Value"',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(114,'2010-10-20 12:24:48.619326',1,10,'131','V trans:Камера недоступна -en:English-> The camera is not available',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(115,'2010-10-20 12:25:42.748144',1,10,'131','V trans:Камера недоступна -en:English-> Camera is unavailable',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(116,'2010-10-20 12:29:37.639355',1,10,'130','V trans:Обучение новой персоной -en:English-> Training of new person',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(117,'2010-10-20 12:30:08.964373',1,10,'129','V trans:Обучение персоны -en:English-> Training person',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(118,'2010-10-20 12:30:34.154093',1,10,'6','V trans:Обучение -en:English-> Training',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(119,'2010-10-20 12:31:03.146182',1,10,'20','V trans:Обучение базы персон -en:English-> Training database of persons',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(120,'2010-10-20 12:31:44.767333',1,10,'128','V trans:Выберите персону из базы, пожалуйста -en:English-> Select a person from the database, please',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(121,'2010-10-20 12:32:18.644034',1,10,'127','V trans:Введите имя персоны, пожалуйста -en:English-> Enter the name of the person, please',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(122,'2010-10-20 12:32:38.354378',1,10,'126','V trans:Введено слишком большое значение -en:English-> Introduced too much',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(123,'2010-10-20 12:33:00.064100',1,10,'119','V trans:Введена слишком большая высота для области захвата -en:English-> Put too great a height for the capture region',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(124,'2010-10-20 12:33:27.802103',1,10,'118','V trans:Введено слишком большое смещение по координате -en:English-> Introduced too much bias in the coordinate',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(125,'2010-10-20 12:33:53.746453',1,10,'117','V trans:Введена слишком большая ширина для области захвата -en:English-> Put too much width to the capture region',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(126,'2010-10-20 12:34:15.376521',1,10,'116','V trans:Значение должно содержать только цифры -en:English-> The value must contain only numbers',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(127,'2010-10-20 12:34:59.462562',1,10,'115','V trans:Выберите, пожалуйста, хотя бы одно изображение -en:English-> Please select at least one image',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(128,'2010-10-20 12:36:26.369030',1,10,'114','V trans:Вы, действительно, хотите удалить базу персон -en:English-> Want you delete the database of persons',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(129,'2010-10-20 12:37:07.299026',1,10,'113','V trans:Вы, действительно, хотите удалить выбранные фотографии -en:English-> Want you delete the selected photos',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(130,'2010-10-20 12:37:57.876131',1,10,'112','V trans:шт -en:English-> pcs',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(131,'2010-10-20 12:39:10.407519',1,10,'111','V trans:Вы, действительно, хотите удалить выбранных персон -en:English-> Want you delete the selected persons',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(132,'2010-10-20 12:39:35.049115',1,10,'110','V trans:Выберите, пожалуйста, хотя бы одну фотографию персоны -en:English-> Please select at least one photograph of the person',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(133,'2010-10-20 12:39:57.312001',1,10,'109','V trans:Выберите, пожалуйста, хотя бы одну персону -en:English-> Please select at least one person',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(134,'2010-10-20 12:40:40.685440',1,10,'39','V trans:Предупреждение -en:English-> Warning',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(135,'2010-10-20 12:41:16.629845',1,10,'21','V trans:Вы можете загрузить -en:English-> You can download',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(136,'2010-10-20 12:41:46.806521',1,10,'2','V trans:Выбор языка -en:English-> Select language',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(137,'2010-10-20 12:42:21.489860',1,10,'22','V trans:файлы форматов -en:English-> file formats',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(138,'2010-10-20 12:42:45.669534',1,10,'23','V trans:видео формата -en:English-> video format',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(139,'2010-10-20 12:43:48.191089',1,10,'24','V trans:Обучить новой персоной -en:English-> Traning a new person',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(140,'2010-10-20 12:44:24.135046',1,10,'27','V trans:Обучить с камеры -en:English-> Train with the camera',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(141,'2010-10-20 12:45:46.967471',1,10,'108','V trans:Параметр не применился. Пожалуйста, попробуйте ещё раз -en:English-> Parameter does not apply. Please try again',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(142,'2010-10-20 12:46:15.813582',1,10,'105','V trans:Пожалуйста, попробуйте подключиться позднее -en:English-> Please try connecting again later',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(143,'2010-10-20 12:46:50.416991',1,10,'104','V trans:недоступен -en:English-> unavailable',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(144,'2010-10-20 12:47:42.646210',1,10,'103','V trans:Ошибка подключения! -en:English-> Connection error!',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(145,'2010-10-20 12:48:10.198092',1,10,'101','V trans:Введите максимальное количество камер, которое должен найти коммуникатор -en:English-> Enter the maximum number of cameras, which must find a communicator',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(146,'2010-10-20 12:48:34.299790',1,10,'100','V trans:Обновление списка камер -en:English-> Updating list of cameras',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(147,'2010-10-20 12:48:58.378411',1,10,'99','V trans:Камера выкл. -en:English-> Camera off.',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(148,'2010-10-20 12:49:28.485717',1,10,'98','V trans:Идент. лиц -en:English-> Ident. persons',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(149,'2010-10-20 12:49:51.554766',1,10,'97','V trans:Детект. лиц -en:English-> Detective. persons',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(150,'2010-10-20 12:50:16.140534',1,10,'96','V trans:Видео режим -en:English-> Video mode',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(151,'2010-10-20 12:50:44.772865',1,10,'95','V trans:Название камеры -en:English-> Camera title',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(152,'2010-10-20 12:51:29.642270',1,10,'31','V trans:Выбрать персону из базы -en:English-> Choose a person from the database',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(153,'2010-10-20 12:51:50.255769',1,10,'30','V trans:Загрузите файлы -en:English-> Upload files',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(154,'2010-10-20 12:52:15.671886',1,10,'29','V trans:Назад -en:English-> Back',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(155,'2010-10-20 12:52:38.022146',1,10,'28','V trans:Загрузить файлы -en:English-> Upload Files',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(156,'2010-10-20 12:53:45.923380',1,10,'30','V trans:Загрузите файлы -en:English-> Please upload files',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(157,'2010-10-20 12:54:10.632032',1,10,'26','V trans:Выберите персону -en:English-> Select a person',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(158,'2010-10-20 12:54:51.228103',1,10,'36','V trans:Закрыть окно -en:English-> Close the window',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(159,'2010-10-20 12:55:20.367444',1,10,'38','V trans:Далее -en:English-> Next',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(160,'2010-10-20 12:56:04.502631',1,10,'94','V trans:Режим сервера -en:English-> Server mode',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(161,'2010-10-20 12:56:32.294943',1,10,'93','V trans:Список камер -en:English-> List chambers',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(162,'2010-10-20 12:57:47.096232',1,10,'83','V trans:Количество кадров -en:English-> Number of frames',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(163,'2010-10-20 12:58:35.024730',1,10,'92','V trans:Выберите коммуникатор -en:English-> Select device',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(164,'2010-10-20 12:58:54.852042',1,10,'91','V trans:Для загрузки сохранённых настроек для всех камер выбранного коммуникатора -en:English-> To load the saved settings for all cameras selected device',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(165,'2010-10-20 12:59:26.622394',1,10,'90','V trans:Загрузить настройки -en:English-> Load settings',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(166,'2010-10-20 12:59:49.362570',1,10,'88','V trans:Сохранить профиль -en:English-> Save settings',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(167,'2010-10-20 13:00:12.109744',1,10,'89','V trans:Для сохранения настроек для всех камер выбранного коммуникатора -en:English-> To save your settings for all cameras selected device',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(168,'2010-10-20 13:00:37.496069',1,10,'87','V help:Настройки распознавания -en:English-> Configuration identification',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(169,'2010-10-20 13:00:58.975235',1,10,'86','V trans:Расстояние между глаз -en:English-> The distance between the eyes',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(170,'2010-10-20 13:01:52.225805',1,10,'82','V trans:Смещение по -en:English-> Offset',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(171,'2010-10-20 13:02:12.870583',1,10,'81','V trans:Интенсивность -en:English-> Intensity',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(172,'2010-10-20 13:02:31.071410',1,10,'80','V trans:Выпуклость -en:English-> Bulge',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(173,'2010-10-20 13:03:36.352733',1,10,'79','V trans:Дисторсия -en:English-> Distortion',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(174,'2010-10-20 13:03:58.847173',1,10,'78','V trans:Область захвата -en:English-> Capture area',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(175,'2010-10-20 13:04:23.691358',1,10,'77','V trans:Разрешение камеры -en:English-> Camera resolution',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(176,'2010-10-20 13:04:53.462293',1,10,'76','V trans:Разрешение камеры и область захвата -en:English-> Resolution of the camera and capture area',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(177,'2010-10-20 13:10:34.101208',1,10,'75','V trans:Ночной режим -en:English-> Night mode',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(178,'2010-10-20 13:11:54.215562',1,10,'74','V trans:Дневной режим -en:English-> Day mode',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(179,'2010-10-20 13:12:09.574866',1,10,'73','V trans:Ночь -en:English-> Night',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(180,'2010-10-20 13:12:24.254156',1,10,'72','V trans:День -en:English-> Day',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(181,'2010-10-20 13:41:02.537361',1,10,'71','V trans:Частота -en:English-> Frequency',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(182,'2010-10-20 13:41:25.995582',1,10,'37','V trans:Удаление -en:English-> Removing',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(183,'2010-10-20 13:41:49.130225',1,10,'69','V trans:Качественно -en:English-> Qualitatively',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(184,'2010-10-20 13:42:08.993488',1,10,'68','V trans:Сбалансировано -en:English-> Balanced',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(185,'2010-10-20 13:42:29.919665',1,10,'67','V trans:Быстро -en:English-> Quickly',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(186,'2010-10-20 13:42:53.005809',1,10,'66','V trans:Время экспозиции -en:English-> Exposure time',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(187,'2010-10-20 13:43:20.142212',1,10,'65','V trans:Режим низкой освещённости -en:English-> Low light Mode',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(188,'2010-10-20 13:43:40.012668',1,10,'64','V trans:Смешанный -en:English-> Mixed',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(189,'2010-10-20 13:44:10.131054',1,10,'50','V trans:Настройка сервера -en:English-> Server configuration',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(190,'2010-10-20 13:44:29.950803',1,10,'63','V trans:Снаружи помещения -en:English-> Outdoors',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(191,'2010-10-20 13:44:50.021049',1,10,'62','V trans:Внутри помещения -en:English-> Indoors',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(192,'2010-10-20 13:45:13.647117',1,10,'61','V trans:Автоматический -en:English-> Auto',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(193,'2010-10-20 13:45:38.857527',1,10,'60','V trans:Режим освещения -en:English-> Mode lighting',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(194,'2010-10-20 13:45:57.909418',1,10,'59','V trans:Качество -en:English-> Quality',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(195,'2010-10-20 13:46:16.759040',1,10,'58','V trans:Контраст -en:English-> Contrast',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(196,'2010-10-20 13:46:34.349210',1,10,'57','V trans:Насыщенность -en:English-> Saturation',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(197,'2010-10-20 13:46:54.430350',1,10,'56','V trans:Резкость -en:English-> Harshness',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(198,'2010-10-20 13:47:16.731636',1,10,'55','V trans:Применить -en:English-> Apply',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(199,'2010-10-20 13:47:39.909197',1,10,'51','V trans:Настройка камеры -en:English-> Setting the camera',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(200,'2010-10-20 13:48:03.975892',1,10,'52','V trans:Коммуникатор -en:English-> Communicator',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(201,'2010-10-20 13:48:37.243163',1,10,'54','V trans:Яркость -en:English-> Brightness',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(202,'2010-10-20 13:48:53.768311',1,10,'53','V trans:Изображение -en:English-> Image',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(203,'2010-10-20 13:49:14.321460',1,10,'40','V trans:Обнуление базы -en:English-> Resetting the base',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(204,'2010-10-21 07:24:09.399032',1,10,'159','V help:Персона -en:English-> Person',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(205,'2010-10-21 07:24:31.806459',1,10,'143','V help:Настройки камеры -en:English-> The camera settings',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(206,'2010-10-21 07:24:45.423523',1,10,'85','V help:Настройки камер -en:English-> Camera settings',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(207,'2010-10-21 07:24:58.606991',1,10,'47','V help:Идентификация -en:English-> Identification',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(208,'2010-10-21 07:25:14.909479',1,10,'32','V help:Обучение базы персон -en:English-> Training database of persons',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(209,'2010-10-21 07:25:25.172898',1,10,'48','V help:Помощь -en:English-> Help',2,'Changed active.');
INSERT INTO "django_admin_log" VALUES(210,'2010-10-21 07:25:38.493888',1,10,'10','V help:Персоны -en:English-> Persons',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(211,'2010-10-21 07:25:55.410644',1,10,'9','V help:Главная страница помощи -en:English-> Main page of help',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(212,'2010-10-21 07:26:46.432188',1,10,'96','V trans:Видео режим -en:English-> Video',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(213,'2010-10-21 07:27:31.006134',1,10,'97','V trans:Детект. лиц -en:English-> Face detect',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(214,'2010-10-21 07:27:57.647435',1,10,'98','V trans:Идент. лиц -en:English-> Face ident.',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(215,'2010-10-21 07:28:16.701443',1,10,'99','V trans:Камера выкл. -en:English-> Camera off',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(216,'2010-10-21 07:31:26.647417',1,10,'184','V trans:Создать персону -en:English-> Create a person',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(217,'2010-10-21 07:53:54.421623',1,10,'186','V trans:Просмотр видео -en:English-> View',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(218,'2010-10-21 08:07:42.930487',1,10,'185','V trans:Найти персону -en:English-> Find person',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(219,'2010-10-21 08:18:39.762358',1,10,'161','V trans:Найти камеры -en:English-> Find camera',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(220,'2010-10-21 08:19:35.140897',1,10,'49','V trans:Настройки камеры -en:English-> The camera settings',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(221,'2010-10-21 08:21:29.499514',1,10,'1','V trans:Настройки камер -en:English-> Camera settings',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(222,'2010-10-21 10:12:15.482579',1,12,'9','192.168.0.235:13600',2,'Changed port.');
INSERT INTO "django_admin_log" VALUES(223,'2010-10-21 10:12:24.518944',1,12,'9','192.168.0.235:12600',2,'Changed port.');
INSERT INTO "django_admin_log" VALUES(224,'2010-10-21 10:12:30.587246',1,12,'7','192.168.0.235:13600',2,'Changed port.');
INSERT INTO "django_admin_log" VALUES(225,'2010-10-21 10:20:05.601438',1,10,'34','V trans:Настройки распознавания -en:English-> Recognition settings',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(226,'2010-10-21 10:21:09.920591',1,10,'87','V help:Настройки распознавания -en:English-> Recognition settings',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(227,'2010-10-21 10:25:08.153740',1,10,'22','V trans:файлы форматов -en:English-> image formats',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(228,'2010-10-21 10:26:51.149133',1,10,'22','V trans:файлы форматов -en:English-> format image',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(229,'2010-10-21 10:27:15.002622',1,10,'23','V trans:видео формата -en:English-> format video',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(230,'2010-10-21 10:39:00.688661',1,10,'152','V trans:При идентификации -en:English-> In the face recognition',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(231,'2010-10-21 10:39:42.703069',1,10,'151','V trans:При детектировании -en:English-> In the face identification',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(232,'2010-10-21 11:30:25.144213',1,13,'1','192.168.0.237:16544 lLogin pPassword communicator',2,'Changed host.');
INSERT INTO "django_admin_log" VALUES(233,'2010-10-21 11:40:04.440235',1,13,'1','192.168.0.55:16544 lLogin pPassword communicator',2,'Changed host.');
INSERT INTO "django_admin_log" VALUES(234,'2010-10-21 11:46:34.354745',1,13,'1','192.168.0.237:16544 lLogin pPassword communicator',2,'Changed host.');
INSERT INTO "django_admin_log" VALUES(235,'2010-10-21 12:11:14.704451',1,12,'10','192.168.0.237:16544',1,'');
INSERT INTO "django_admin_log" VALUES(236,'2010-10-21 12:21:16.282936',1,13,'1','192.168.0.55:16544 lLogin pPassword communicator',2,'Changed host.');
INSERT INTO "django_admin_log" VALUES(237,'2010-10-21 14:13:22.621067',1,10,'187','V trans:Настроить -en:English-> Customize',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(238,'2010-10-21 14:14:11.637160',1,10,'188','V trans:Минимальный размер лица -en:English-> Min face width',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(239,'2010-10-21 14:14:58.011190',1,10,'189','V trans:Настройка сервера  -en:English-> Server settings',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(240,'2010-10-21 14:17:52.624238',1,10,'190','V trans:Настройка дисторсии -en:English-> Settings distortion',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(241,'2010-10-21 14:18:03.617230',1,10,'191','V help:Настройки дисторсии -en:English-> Settings distortion',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(242,'2010-10-21 14:18:13.770294',1,10,'193','V trans:Настройки дисторсии -en:English-> Settings distortion',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(243,'2010-10-21 16:10:04.240851',1,10,'198','V trans:Обучение с камеры -en:English-> Trening from the camera',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(244,'2010-10-21 16:10:42.063576',1,10,'196','V trans:Выбор -en:English-> Choose',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(245,'2010-10-21 16:10:55.758270',1,10,'194','V trans:Выбор камеры -en:English-> Choose camera',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(246,'2010-10-21 16:11:51.571193',1,10,'195','V help:Выбор камеры для обучения -en:English-> Choose camera for training',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(247,'2010-10-21 16:12:29.257418',1,10,'198','V trans:Обучение с камеры -en:English-> Training from the camera',2,'Changed translate.');
INSERT INTO "django_admin_log" VALUES(248,'2010-10-21 16:13:04.664637',1,10,'199','V trans:Ошибка подключения! Камера с таким названием недоступна. Пожалуйста, попробуйте подключиться позднее -en:English-> Connection Error! Camera with such a title is not available. Please try conne',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(249,'2010-10-22 10:42:26.595267',1,13,'1','192.168.0.237:16544 lLogin pPassword communicator',2,'Изменен host.');
INSERT INTO "django_admin_log" VALUES(250,'2010-10-22 12:07:52.907105',1,13,'1','192.168.0.55:16544 lLogin pPassword communicator',2,'Изменен host.');
INSERT INTO "django_admin_log" VALUES(251,'2010-10-22 12:16:36.071616',1,10,'202','V trans:Версия -en:English-> Version',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(252,'2010-10-22 12:16:59.342908',1,10,'201','V trans:Камера не выбрана -en:English-> The camera is not selected',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(253,'2010-10-22 12:17:23.569240',1,10,'200','V trans:Пожалуйста, подождите -en:English-> Please wait',2,'Changed translate and active.');
INSERT INTO "django_admin_log" VALUES(254,'2010-10-22 12:22:40.885012',1,13,'1','192.168.0.235:16544 lLogin pPassword communicator',2,'Changed host.');
INSERT INTO "django_admin_log" VALUES(255,'2010-10-22 14:06:14.299980',1,13,'1','192.168.0.237:16544 lLogin pPassword communicator',2,'Изменен host.');
INSERT INTO "django_admin_log" VALUES(256,'2010-10-27 07:53:30.498185',1,13,'1','192.168.0.55:16544 lLogin pPassword communicator',2,'Изменен host.');
INSERT INTO "django_admin_log" VALUES(257,'2010-10-28 09:49:30.907967',1,13,'1','192.168.0.237:16544 lLogin pPassword communicator',2,'Изменен host.');
INSERT INTO "django_admin_log" VALUES(258,'2010-10-28 09:50:50.082137',1,13,'1','192.168.0.55:16544 lLogin pPassword communicator',2,'Изменен host.');
INSERT INTO "django_admin_log" VALUES(259,'2010-11-13 19:16:44.253700',1,27,'1','192.168.0.15 AV2100 Главный вход',2,'Изменен kpp.');
INSERT INTO "django_admin_log" VALUES(260,'2010-11-13 19:57:58.485037',1,29,'3','login_timeout = 60',2,'Изменен value.');
INSERT INTO "django_admin_log" VALUES(261,'2010-11-13 22:39:09.587367',1,29,'2','wait_unidentified_person = 5',2,'Изменен value.');
INSERT INTO "django_admin_log" VALUES(262,'2010-11-13 22:49:13.667913',1,29,'2','wait_unidentified_person = 10',2,'Изменен value.');
INSERT INTO "django_admin_log" VALUES(263,'2010-11-13 22:52:08.947135',1,29,'1','last_journal_update = 10',2,'Изменен value.');
INSERT INTO "django_admin_log" VALUES(264,'2010-11-13 22:56:59.523134',1,29,'3','journalBoundCoeff = 0.41',2,'Изменен value.');
INSERT INTO "django_admin_log" VALUES(265,'2010-11-15 11:13:47.248966',1,27,'1','192.168.0.15 AV2100 Главный вход',2,'Изменен position.');
INSERT INTO "django_admin_log" VALUES(266,'2010-11-15 15:09:05.303912',1,29,'2','wait_unidentified_person = 10',2,'Изменен value.');
INSERT INTO "django_admin_log" VALUES(267,'2010-11-15 15:09:11.315025',1,29,'1','last_journal_update = 10',2,'Изменен value.');
INSERT INTO "django_admin_log" VALUES(268,'2010-11-15 15:13:45.163501',1,29,'2','wait_unidentified_person = 10',2,'Изменен value.');
INSERT INTO "django_admin_log" VALUES(269,'2010-11-15 15:15:51.347671',1,29,'2','wait_unidentified_person = 5',2,'Изменен value.');
INSERT INTO "django_admin_log" VALUES(270,'2010-11-15 15:52:14.034132',1,29,'3','journalBoundCoeff = 0.41',2,'Изменен value.');
INSERT INTO "django_admin_log" VALUES(271,'2010-11-15 15:52:19.298906',1,29,'2','wait_unidentified_person = 10',2,'Изменен value.');
INSERT INTO "django_admin_log" VALUES(272,'2010-11-15 15:52:24.238330',1,29,'1','last_journal_update = 10',2,'Изменен value.');
CREATE TABLE "videoclient_communicator" (
    "id" integer NOT NULL PRIMARY KEY,
    "host" varchar(32) NOT NULL,
    "port" integer NOT NULL,
    "active" bool NOT NULL
);
INSERT INTO "videoclient_communicator" VALUES(1,'192.168.0.55',12600,1);
INSERT INTO "videoclient_communicator" VALUES(2,'192.168.0.55',13600,1);
INSERT INTO "videoclient_communicator" VALUES(3,'192.168.0.55',14600,1);
INSERT INTO "videoclient_communicator" VALUES(4,'192.168.0.123',12600,1);
INSERT INTO "videoclient_communicator" VALUES(5,'192.168.0.123',13600,1);
INSERT INTO "videoclient_communicator" VALUES(6,'192.168.0.123',14600,1);
INSERT INTO "videoclient_communicator" VALUES(7,'192.168.0.235',13600,1);
INSERT INTO "videoclient_communicator" VALUES(8,'192.168.0.235',16544,1);
INSERT INTO "videoclient_communicator" VALUES(9,'192.168.0.235',12600,1);
INSERT INTO "videoclient_communicator" VALUES(10,'192.168.0.237',16544,1);
CREATE TABLE "videoclient_balancer" (
    "id" integer NOT NULL PRIMARY KEY,
    "host" varchar(32) NOT NULL,
    "port" integer NOT NULL,
    "login" varchar(32) NOT NULL,
    "passwd" varchar(32) NOT NULL,
    "user" varchar(32) NOT NULL,
    "active" bool NOT NULL
);
INSERT INTO "videoclient_balancer" VALUES(1,'192.168.0.55',16544,'lLogin','pPassword','communicator',1);
CREATE TABLE "videoclient_divisionuser" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(32) NOT NULL
);
INSERT INTO "videoclient_divisionuser" VALUES(1,'Операторы');
INSERT INTO "videoclient_divisionuser" VALUES(2,'Посетители');
INSERT INTO "videoclient_divisionuser" VALUES(3,'Персоны');
INSERT INTO "videoclient_divisionuser" VALUES(4,'Сотрудники');
CREATE TABLE "videoclient_positionuser" (
    "id" integer NOT NULL PRIMARY KEY,
    "division_id" integer REFERENCES "videoclient_divisionuser" ("id"),
    "name" varchar(32) NOT NULL
);
INSERT INTO "videoclient_positionuser" VALUES(1,NULL,'Программист');
INSERT INTO "videoclient_positionuser" VALUES(2,NULL,'Охранник');
INSERT INTO "videoclient_positionuser" VALUES(3,NULL,'Адвокат');
INSERT INTO "videoclient_positionuser" VALUES(4,NULL,'Следователь');
INSERT INTO "videoclient_positionuser" VALUES(5,NULL,'Секретарь');
CREATE TABLE "videoclient_statususer" (
    "id" integer NOT NULL PRIMARY KEY,
    "division_id" integer REFERENCES "videoclient_divisionuser" ("id"),
    "name" varchar(32) NOT NULL
);
INSERT INTO "videoclient_statususer" VALUES(1,1,'Оператор');
INSERT INTO "videoclient_statususer" VALUES(2,1,'Администратор');
INSERT INTO "videoclient_statususer" VALUES(3,1,'Доступ запрещен');
INSERT INTO "videoclient_statususer" VALUES(4,3,'Подследственный');
INSERT INTO "videoclient_statususer" VALUES(5,3,'Осужденный');
INSERT INTO "videoclient_statususer" VALUES(6,2,'Адвокат');
INSERT INTO "videoclient_statususer" VALUES(7,2,'Следователь');
INSERT INTO "videoclient_statususer" VALUES(8,2,'Родственник');
INSERT INTO "videoclient_statususer" VALUES(9,4,'Адвокат');
INSERT INTO "videoclient_statususer" VALUES(10,4,'Следователь');
INSERT INTO "videoclient_statususer" VALUES(11,4,'Секретарь');
CREATE TABLE "videoclient_kpp" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(32) NOT NULL
);
INSERT INTO "videoclient_kpp" VALUES(1,'Главный вход');
CREATE TABLE "videoclient_document" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(32) NOT NULL
);
INSERT INTO "videoclient_document" VALUES(1,'Паспорт');
INSERT INTO "videoclient_document" VALUES(2,'Удостоверение');
CREATE TABLE "videoclient_category" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(32) NOT NULL
);
INSERT INTO "videoclient_category" VALUES(1,'Опасен');
INSERT INTO "videoclient_category" VALUES(2,'Особо опасен');
INSERT INTO "videoclient_category" VALUES(3,'Рецидивист');
CREATE TABLE "videoclient_user" (
    "user_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "auth_user" ("id"),
    "middle_name" varchar(32) NOT NULL,
    "birthday" date,
    "passport_series" varchar(8) NOT NULL,
    "passport_number" varchar(16) NOT NULL,
    "passport_note" text NOT NULL,
    "passport_date" date,
    "address" text NOT NULL,
    "phone_work" varchar(32) NOT NULL,
    "phone_home" varchar(32) NOT NULL,
    "phone_mobile" varchar(32) NOT NULL,
    "note" text NOT NULL,
    "division_id" integer REFERENCES "videoclient_divisionuser" ("id"),
    "position_id" integer REFERENCES "videoclient_positionuser" ("id"),
    "status_id" integer REFERENCES "videoclient_statususer" ("id"),
    "kpp_id" integer REFERENCES "videoclient_kpp" ("id"),
    "staff" integer,
    "last_access" datetime NOT NULL
);
INSERT INTO "videoclient_user" VALUES(2,'',NULL,'','','',NULL,'','','','','',1,NULL,1,1,2,'2010-11-13 22:44:06.662059');
INSERT INTO "videoclient_user" VALUES(3,'',NULL,'','','',NULL,'','','','','',1,NULL,2,1,3,'2010-11-13 20:43:54.634099');
INSERT INTO "videoclient_user" VALUES(4,'',NULL,'','','',NULL,'','','','','',1,NULL,1,1,6,'2010-11-15 15:02:17.543314');
INSERT INTO "videoclient_user" VALUES(5,'',NULL,'','','',NULL,'','','','','',1,NULL,1,1,5,'2010-11-15 15:02:35.327566');
INSERT INTO "videoclient_user" VALUES(6,'',NULL,'','','',NULL,'','','','','',1,NULL,1,1,3,'2010-11-15 15:03:16.267269');
INSERT INTO "videoclient_user" VALUES(7,'',NULL,'','','',NULL,'','','','','',1,NULL,1,1,2,'2010-11-15 15:03:30.998233');
INSERT INTO "videoclient_user" VALUES(8,'',NULL,'','','',NULL,'','','','','',1,NULL,1,1,2,'2010-11-15 15:03:42.801943');
INSERT INTO "videoclient_user" VALUES(9,'',NULL,'','','',NULL,'','','','','',1,NULL,1,1,2,'2010-11-15 15:03:52.289618');
INSERT INTO "videoclient_user" VALUES(10,'',NULL,'','','',NULL,'','','','','',1,NULL,1,1,3,'2010-11-15 15:04:05.203976');
INSERT INTO "videoclient_user" VALUES(11,'',NULL,'','','',NULL,'','','','','',1,NULL,1,1,3,'2010-11-15 15:04:18.615721');
INSERT INTO "videoclient_user" VALUES(12,'',NULL,'','','',NULL,'','','','','',1,NULL,1,1,3,'2010-11-15 15:04:29.883809');
INSERT INTO "videoclient_user" VALUES(13,'',NULL,'','','',NULL,'','','','','',1,NULL,1,1,3,'2010-11-15 15:04:43.021807');
INSERT INTO "videoclient_user" VALUES(14,'',NULL,'','','',NULL,'','','','','',1,NULL,1,1,3,'2010-11-15 15:04:54.142422');
INSERT INTO "videoclient_user" VALUES(15,'',NULL,'','','',NULL,'','','','','',1,NULL,1,1,6,'2010-11-15 15:05:41.946633');
INSERT INTO "videoclient_user" VALUES(16,'',NULL,'','','',NULL,'','','','','',1,NULL,1,1,6,'2010-11-15 15:05:57.577571');
INSERT INTO "videoclient_user" VALUES(17,'',NULL,'','','',NULL,'','','','','',1,NULL,1,1,5,'2010-11-15 15:06:10.945640');
CREATE TABLE "videoclient_loginjournal" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "videoclient_user" ("user_ptr_id"),
    "login" datetime NOT NULL,
    "logout" datetime
);
INSERT INTO "videoclient_loginjournal" VALUES(1,2,'2010-11-13 19:50:58.794377','2010-11-13 19:50:59.554686');
INSERT INTO "videoclient_loginjournal" VALUES(2,2,'2010-11-13 19:58:46.865610','2010-11-13 19:59:47.042160');
INSERT INTO "videoclient_loginjournal" VALUES(3,2,'2010-11-13 20:02:03.043043','2010-11-13 20:03:06.618185');
INSERT INTO "videoclient_loginjournal" VALUES(4,2,'2010-11-13 20:11:05.117000','2010-11-13 20:12:20.821133');
INSERT INTO "videoclient_loginjournal" VALUES(5,2,'2010-11-13 20:12:26.996197','2010-11-13 20:12:36.667039');
INSERT INTO "videoclient_loginjournal" VALUES(6,2,'2010-11-13 20:12:41.616467','2010-11-13 20:13:45.150924');
INSERT INTO "videoclient_loginjournal" VALUES(7,2,'2010-11-13 20:18:14.893492','2010-11-13 20:18:56.157889');
INSERT INTO "videoclient_loginjournal" VALUES(8,3,'2010-11-13 20:22:07.100943','2010-11-13 20:22:07.275080');
INSERT INTO "videoclient_loginjournal" VALUES(9,3,'2010-11-13 20:22:13.936917','2010-11-13 20:22:14.026479');
INSERT INTO "videoclient_loginjournal" VALUES(10,3,'2010-11-13 20:26:46.807002','2010-11-13 20:27:58.917894');
INSERT INTO "videoclient_loginjournal" VALUES(11,2,'2010-11-13 20:28:10.212264','2010-11-13 20:28:18.078239');
INSERT INTO "videoclient_loginjournal" VALUES(12,2,'2010-11-13 20:31:34.763556','2010-11-13 20:34:09.510576');
INSERT INTO "videoclient_loginjournal" VALUES(13,2,'2010-11-13 20:34:38.623746','2010-11-13 20:35:43.342443');
INSERT INTO "videoclient_loginjournal" VALUES(14,2,'2010-11-13 20:36:10.872457','2010-11-13 20:37:40.002881');
INSERT INTO "videoclient_loginjournal" VALUES(15,3,'2010-11-13 20:37:46.121287','2010-11-13 20:44:54.634099');
INSERT INTO "videoclient_loginjournal" VALUES(16,2,'2010-11-13 20:41:38.917935','2010-11-13 20:42:07.627647');
INSERT INTO "videoclient_loginjournal" VALUES(17,2,'2010-11-13 22:34:50.197371','2010-11-13 23:14:06.662059');
CREATE TABLE "videoclient_groupperson" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(32) NOT NULL
);
CREATE TABLE "videoclient_person" (
    "id" integer NOT NULL PRIMARY KEY,
    "id_person" integer,
    "date" datetime NOT NULL,
    "user_id" integer REFERENCES "videoclient_user" ("user_ptr_id"),
    "action" integer unsigned NOT NULL,
    "first_name" varchar(32) NOT NULL,
    "last_name" varchar(32) NOT NULL,
    "middle_name" varchar(32) NOT NULL,
    "birthday" date,
    "passport_series" varchar(8) NOT NULL,
    "passport_number" varchar(16) NOT NULL,
    "passport_note" text NOT NULL,
    "passport_date" date,
    "address" text NOT NULL,
    "phone_work" varchar(32) NOT NULL,
    "phone_home" varchar(32) NOT NULL,
    "phone_mobile" varchar(32) NOT NULL,
    "note" text NOT NULL,
    "group_id" integer REFERENCES "videoclient_groupperson" ("id"),
    "status_id" integer REFERENCES "videoclient_statususer" ("id"),
    "goto" integer unsigned NOT NULL,
    "document_id" integer REFERENCES "videoclient_document" ("id"),
    "passport_code" varchar(8),
    "address_temp" text NOT NULL,
    "category_id" integer REFERENCES "videoclient_category" ("id"),
    "number" varchar(32),
    "article" varchar(128),
    "article_part" varchar(32),
    "article_item" varchar(32),
    "room_facility" varchar(32)
);
INSERT INTO "videoclient_person" VALUES(1,1,'2010-11-13 19:14:30.239563',NULL,0,'Шилов','Дмитри','Игоревич',NULL,'12','312','343444',NULL,'','','','','',NULL,6,0,1,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(2,2,'2010-11-13 19:15:47.882613',NULL,0,'Иванов','Дмитрий','Ивановвич',NULL,'','','',NULL,'','','','','',NULL,9,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(3,3,'2010-11-13 20:19:57.689596',NULL,0,'Сергеев','Сергей','Сергеевич',NULL,'','','',NULL,'','','','','',NULL,10,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(4,2,'2010-11-13 20:57:09.153327',NULL,1,'Иванов','Дмитрий','Ивановвич',NULL,'','','',NULL,'','','','','',NULL,9,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(5,2,'2010-11-13 20:59:21.645861',NULL,1,'Иванов','Дмитрий','Ивановвич',NULL,'','','',NULL,'','','','','',NULL,9,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(6,2,'2010-11-13 20:59:47.407144',NULL,1,'Иванов','Дмитрий','Ивановвич',NULL,'','','',NULL,'','','','','',NULL,9,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(7,3,'2010-11-13 21:34:02.124478',NULL,1,'Сергеев','Сергей','Сергеевич',NULL,'','','',NULL,'','','','','',NULL,10,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(8,1,'2010-11-13 22:19:46.745997',NULL,1,'Шилов','Дмитри','Игоревич',NULL,'12','312','343444',NULL,'','','','','',NULL,6,0,1,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(9,1,'2010-11-13 22:27:10.595115',NULL,1,'Мина','Солтан','М',NULL,'12','312','343444',NULL,'','','','','',NULL,6,0,1,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(10,1,'2010-11-13 22:38:58.028174',NULL,1,'Мина','Солтан','М',NULL,'12','312','343444',NULL,'','','','','',NULL,6,0,1,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(11,4,'2010-11-13 22:41:34.331254',NULL,0,'Иванов','Иван','Иванович','1975-09-17','1255','963258','Советским ОВД',NULL,'Череповец, металлургов 22-22','','','','',NULL,7,0,1,'030-56','Вологда, Гагарина 4-56',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(12,5,'2010-11-13 22:53:49.503006',NULL,0,'Шилов','Дима','И',NULL,'','','',NULL,'','','','','',NULL,10,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(13,4,'2010-11-13 22:57:28.436070',NULL,1,'Иванов','Иван','Иванович','1975-09-17','1255','963258','Советским ОВД',NULL,'Череповец, металлургов 22-22','','','','',NULL,7,0,1,'030-56','Вологда, Гагарина 4-56',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(14,6,'2010-11-15 12:26:21.092037',NULL,0,'Белова','Юлия','',NULL,'','','',NULL,'','','','','',NULL,10,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(15,7,'2010-11-15 12:32:24.667181',NULL,0,'Семенов','Семен','Семенович',NULL,'','','',NULL,'','','','','',NULL,5,0,NULL,'','',2,'123','4453','','','');
INSERT INTO "videoclient_person" VALUES(16,8,'2010-11-15 12:32:54.083228',NULL,0,'4455','234','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(17,9,'2010-11-15 12:33:12.521181',NULL,0,'111','111','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(18,10,'2010-11-15 12:33:24.704868',NULL,0,'222','222','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(19,11,'2010-11-15 12:33:34.210007',NULL,0,'333','333','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(20,12,'2010-11-15 12:33:43.758805',NULL,0,'444','444','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(21,13,'2010-11-15 12:33:53.730131',NULL,0,'555','555','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(22,14,'2010-11-15 12:34:04.155696',NULL,0,'666','666','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(23,15,'2010-11-15 12:34:16.548861',NULL,0,'777','777','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(24,16,'2010-11-15 12:34:26.401092',NULL,0,'888','888','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(25,17,'2010-11-15 12:34:35.731069',NULL,0,'999','999','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(26,18,'2010-11-15 12:34:45.093176',NULL,0,'000','000','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(27,19,'2010-11-15 12:34:59.406919',NULL,0,'111111','111111','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(28,20,'2010-11-15 12:35:13.741681',NULL,0,'121212','121212','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(29,21,'2010-11-15 12:35:27.174529',NULL,0,'131313','131313','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(30,22,'2010-11-15 12:35:38.465226',NULL,0,'141414','141414','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(31,6,'2010-11-15 15:19:06.978044',NULL,1,'Белова','Юлия','',NULL,'','','',NULL,'','','','','',NULL,10,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(32,6,'2010-11-15 16:52:29.143898',NULL,1,'Белова','Юлия2','',NULL,'','','',NULL,'','','','','',NULL,10,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(33,6,'2010-11-15 16:55:48.303204',NULL,1,'Белова','Юлия','',NULL,'','','',NULL,'','','','','',NULL,10,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(34,6,'2010-11-15 16:56:26.663550',NULL,1,'Белова','Юлия','',NULL,'','','',NULL,'','','','','',NULL,10,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(35,6,'2010-11-15 16:58:54.270535',NULL,1,'Белова','Юлия','',NULL,'','','',NULL,'','','','','',NULL,10,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(36,6,'2010-11-15 16:59:07.522995',NULL,1,'Белова','Юлия','',NULL,'','','',NULL,'','','','','',NULL,10,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(37,6,'2010-11-15 17:01:04.839257',NULL,1,'Белова','Юлия2','',NULL,'','','',NULL,'','','','','',NULL,10,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(38,5,'2010-11-15 17:10:18.296763',NULL,1,'Шилов','Дмитрий','Игоревич',NULL,'','','',NULL,'','','','','',NULL,9,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(39,3,'2010-11-15 19:30:08.485554',NULL,3,'Сергеев','Сергей','Сергеевич',NULL,'','','',NULL,'','','','','',NULL,10,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(40,8,'2010-11-15 19:51:50.174537',NULL,1,'Сергеев','Сергей','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(41,8,'2010-11-15 19:51:54.439672',NULL,1,'Сергеев','Сергей','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','','','');
INSERT INTO "videoclient_person" VALUES(42,9,'2010-11-15 19:55:22.801343',NULL,1,'Петров','Петр','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','1','2','');
INSERT INTO "videoclient_person" VALUES(43,10,'2010-11-15 19:56:01.585325',NULL,1,'Петрушин','Игорь','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','58','8','');
INSERT INTO "videoclient_person" VALUES(44,21,'2010-11-15 19:57:10.593343',NULL,1,'Фомин','Александр','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','21','3','');
INSERT INTO "videoclient_person" VALUES(45,11,'2010-11-15 19:57:24.846441',NULL,1,'Трутнев','Александр','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','52','7б','');
INSERT INTO "videoclient_person" VALUES(46,20,'2010-11-15 19:57:36.476594',NULL,1,'Кочешков','Максим','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','43','1','');
INSERT INTO "videoclient_person" VALUES(47,19,'2010-11-15 19:58:00.121031',NULL,1,'Лаптев','Рустам','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','6','2','');
INSERT INTO "videoclient_person" VALUES(48,12,'2010-11-15 19:58:01.946868',NULL,1,'Колпин','Станислав','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','87','79а','');
INSERT INTO "videoclient_person" VALUES(49,18,'2010-11-15 19:58:19.525412',NULL,1,'Спиридонов','Михаил','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','34','5','');
INSERT INTO "videoclient_person" VALUES(50,13,'2010-11-15 19:58:32.304567',NULL,1,'Прутков','Георгий','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','1','5в','');
INSERT INTO "videoclient_person" VALUES(51,17,'2010-11-15 19:58:45.367710',NULL,1,'Стаников','Эдуард','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','22','7','');
INSERT INTO "videoclient_person" VALUES(52,14,'2010-11-15 19:59:00.563446',NULL,1,'Борисов','Аркадий','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','45','63','');
INSERT INTO "videoclient_person" VALUES(53,16,'2010-11-15 19:59:04.090693',NULL,1,'Эшкобин','Всеволод','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','56','3','');
INSERT INTO "videoclient_person" VALUES(54,15,'2010-11-15 19:59:29.047316',NULL,1,'Рубинин','Ростислав','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','46','4','');
INSERT INTO "videoclient_person" VALUES(55,22,'2010-11-15 20:00:14.168667',NULL,1,'Путяйкин','Станислав','',NULL,'','','',NULL,'','','','','',NULL,4,0,NULL,'','',1,'','','33','1','');
INSERT INTO "videoclient_person" VALUES(56,7,'2010-11-15 20:27:14.629928',NULL,1,'Семенов','Семен','Семенович',NULL,'','','',NULL,'','','','','',NULL,5,0,NULL,'','',2,'123','4453','','','');
INSERT INTO "videoclient_person" VALUES(57,2,'2010-11-15 20:56:31.844240',NULL,1,'Иванов','Дмитрий','Ивановвич',NULL,'','','',NULL,'','','','','',NULL,11,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(58,6,'2010-11-15 20:57:02.174581',NULL,1,'Белова','Юлия2','',NULL,'','','',NULL,'','','','','',NULL,11,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(59,5,'2010-11-15 20:57:40.864831',NULL,1,'Шилов','Дмитрий','Игоревич',NULL,'','','',NULL,'','','','','',NULL,11,0,NULL,'','',NULL,'','','','','');
INSERT INTO "videoclient_person" VALUES(60,2,'2010-11-15 20:57:54.171970',NULL,1,'Иванов','Дмитрий','Иванович',NULL,'','','',NULL,'','','','','',NULL,11,0,NULL,'','',NULL,'','','','','');
CREATE TABLE "videoclient_personid" (
    "id" integer NOT NULL PRIMARY KEY,
    "date" date NOT NULL,
    "person_id" integer REFERENCES "videoclient_person" ("id")
, active boolean default 1);
INSERT INTO "videoclient_personid" VALUES(1,'2010-11-13',10,1);
INSERT INTO "videoclient_personid" VALUES(2,'2010-11-15',60,1);
INSERT INTO "videoclient_personid" VALUES(3,'2010-11-13',7,0);
INSERT INTO "videoclient_personid" VALUES(4,'2010-11-13',13,1);
INSERT INTO "videoclient_personid" VALUES(5,'2010-11-15',59,1);
INSERT INTO "videoclient_personid" VALUES(6,'2010-11-15',58,1);
INSERT INTO "videoclient_personid" VALUES(7,'2010-11-15',56,1);
INSERT INTO "videoclient_personid" VALUES(8,'2010-11-15',41,1);
INSERT INTO "videoclient_personid" VALUES(9,'2010-11-15',42,1);
INSERT INTO "videoclient_personid" VALUES(10,'2010-11-15',43,1);
INSERT INTO "videoclient_personid" VALUES(11,'2010-11-15',45,1);
INSERT INTO "videoclient_personid" VALUES(12,'2010-11-15',48,1);
INSERT INTO "videoclient_personid" VALUES(13,'2010-11-15',50,1);
INSERT INTO "videoclient_personid" VALUES(14,'2010-11-15',52,1);
INSERT INTO "videoclient_personid" VALUES(15,'2010-11-15',54,1);
INSERT INTO "videoclient_personid" VALUES(16,'2010-11-15',53,1);
INSERT INTO "videoclient_personid" VALUES(17,'2010-11-15',51,1);
INSERT INTO "videoclient_personid" VALUES(18,'2010-11-15',49,1);
INSERT INTO "videoclient_personid" VALUES(19,'2010-11-15',47,1);
INSERT INTO "videoclient_personid" VALUES(20,'2010-11-15',46,1);
INSERT INTO "videoclient_personid" VALUES(21,'2010-11-15',44,1);
INSERT INTO "videoclient_personid" VALUES(22,'2010-11-15',55,1);
CREATE TABLE "videoclient_rule" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(32) NOT NULL
);
CREATE TABLE "videoclient_rulegroup" (
    "id" integer NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id"),
    "rule_id" integer NOT NULL REFERENCES "videoclient_rule" ("id"),
    "active" bigint NOT NULL
);
CREATE TABLE "videoclient_camera" (
    "id" integer NOT NULL PRIMARY KEY,
    "ip" varchar(15) NOT NULL,
    "type" varchar(8) NOT NULL,
    "kpp_id" integer REFERENCES "videoclient_kpp" ("id"),
    "position" integer unsigned NOT NULL
);
INSERT INTO "videoclient_camera" VALUES(1,'192.168.0.15','AV2100',1,1);
INSERT INTO "videoclient_camera" VALUES(2,'null','null',NULL,0);
CREATE TABLE "videoclient_ground" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(32) NOT NULL
);
INSERT INTO "videoclient_ground" VALUES(1,'Личные вопросы');
INSERT INTO "videoclient_ground" VALUES(2,'Посещение');
INSERT INTO "videoclient_ground" VALUES(3,'Допрос');
INSERT INTO "videoclient_ground" VALUES(4,'Свидание');
INSERT INTO "videoclient_ground" VALUES(5,'Ремонтные работы');
INSERT INTO "videoclient_ground" VALUES(6,'Следственный эксперимент');
INSERT INTO "videoclient_ground" VALUES(7,'Очная ставка');
CREATE TABLE "videoclient_visitingcard" (
    "id" integer NOT NULL PRIMARY KEY,
    "visitor_id" integer NOT NULL REFERENCES "videoclient_personid" ("id"),
    "person_id" integer NOT NULL REFERENCES "videoclient_personid" ("id"),
    "ground_id" integer NOT NULL REFERENCES "videoclient_ground" ("id"),
    "dt_enter" datetime NOT NULL,
    "dt_exit" datetime NOT NULL,
    "dt_open" datetime NOT NULL
);
INSERT INTO "videoclient_visitingcard" VALUES(2,1,2,1,'2010-11-13 18:00:00','2010-11-13 23:50:00','2010-11-13 22:59:45.254819');
INSERT INTO "videoclient_visitingcard" VALUES(3,1,8,1,'2010-11-15 00:00:00','2010-11-15 00:00:00','2010-11-15 15:26:58.574642');
INSERT INTO "videoclient_visitingcard" VALUES(4,1,8,1,'2010-11-14 00:00:00','2010-11-14 00:00:00','2010-11-15 15:27:08.108270');
INSERT INTO "videoclient_visitingcard" VALUES(5,1,8,1,'2010-11-14 00:00:00','2010-11-14 00:00:00','2010-11-15 15:27:17.745662');
INSERT INTO "videoclient_visitingcard" VALUES(6,1,8,1,'2010-11-14 00:00:00','2010-11-14 00:00:00','2010-11-15 15:27:25.842759');
INSERT INTO "videoclient_visitingcard" VALUES(7,1,8,1,'2010-11-14 00:00:00','2010-11-14 00:00:00','2010-11-15 15:27:33.876773');
INSERT INTO "videoclient_visitingcard" VALUES(8,1,8,1,'2010-11-14 00:00:00','2010-11-14 00:00:00','2010-11-15 15:27:41.800077');
INSERT INTO "videoclient_visitingcard" VALUES(9,1,8,1,'2010-11-14 00:00:00','2010-11-14 00:00:00','2010-11-15 15:27:50.669530');
INSERT INTO "videoclient_visitingcard" VALUES(10,1,8,1,'2010-11-14 00:00:00','2010-11-14 00:00:00','2010-11-15 15:28:00.492585');
INSERT INTO "videoclient_visitingcard" VALUES(11,1,8,1,'2010-11-14 00:00:00','2010-11-14 00:00:00','2010-11-15 15:28:09.046036');
INSERT INTO "videoclient_visitingcard" VALUES(12,1,8,1,'2010-11-14 00:00:00','2010-11-14 00:00:00','2010-11-15 15:28:17.774481');
INSERT INTO "videoclient_visitingcard" VALUES(13,1,8,1,'2010-11-14 00:00:00','2010-11-14 00:00:00','2010-11-15 15:28:27.100766');
INSERT INTO "videoclient_visitingcard" VALUES(14,1,8,1,'2010-11-14 00:00:00','2010-11-14 00:00:00','2010-11-15 15:28:36.547383');
INSERT INTO "videoclient_visitingcard" VALUES(15,1,8,1,'2010-11-14 00:00:00','2010-11-14 00:00:00','2010-11-15 15:28:45.518490');
INSERT INTO "videoclient_visitingcard" VALUES(16,1,8,1,'2010-11-14 00:00:00','2010-11-14 00:00:00','2010-11-15 15:28:55.360325');
INSERT INTO "videoclient_visitingcard" VALUES(17,1,8,1,'2010-11-14 00:00:00','2010-11-14 00:00:00','2010-11-15 15:29:06.480846');
CREATE TABLE "videoclient_defaultparams" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(32) NOT NULL,
    "value" varchar(32) NOT NULL
);
INSERT INTO "videoclient_defaultparams" VALUES(1,'last_journal_update','30');
INSERT INTO "videoclient_defaultparams" VALUES(2,'wait_unidentified_person','30');
INSERT INTO "videoclient_defaultparams" VALUES(3,'journalBoundCoeff','0.45');
INSERT INTO "videoclient_defaultparams" VALUES(4,'login_timeout','1800');
CREATE TABLE "videoclient_positionsstatus" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(32) NOT NULL
);
INSERT INTO "videoclient_positionsstatus" VALUES(1,'Вход');
INSERT INTO "videoclient_positionsstatus" VALUES(2,'Выход');
INSERT INTO "videoclient_positionsstatus" VALUES(3,'Не определен');
CREATE TABLE "videoclient_journal" (
    "id" integer NOT NULL PRIMARY KEY,
    "person_id" integer REFERENCES "videoclient_personid" ("id"),
    "camera_id" integer REFERENCES "videoclient_camera" ("id"),
    "coeff" integer NOT NULL,
    "dt_first_fixed" datetime NOT NULL,
    "dt_last_fixed" datetime NOT NULL,
    "original" varchar(100) NOT NULL,
    "finded" varchar(100) NOT NULL,
    "positions_status_id" integer NOT NULL REFERENCES "videoclient_positionsstatus" ("id"),
    "operator_id" integer REFERENCES "videoclient_user" ("user_ptr_id"),
    "dt_open" datetime NOT NULL
);
INSERT INTO "videoclient_journal" VALUES(1,4,1,45,'2010-11-15 19:33:28.160849','2010-11-15 19:35:22.434479','journal//original/2010/11/15/19/33','journal//finded/2010/11/15/19/33',3,NULL,'2010-11-15 19:33:28.458937');
INSERT INTO "videoclient_journal" VALUES(2,NULL,1,36,'2010-11-15 19:37:45.475938','2010-11-15 19:38:59.345020','journal//original/2010/11/15/19/37','journal//finded/2010/11/15/19/37',3,NULL,'2010-11-15 19:37:45.510225');
INSERT INTO "videoclient_journal" VALUES(3,NULL,1,37,'2010-11-15 19:41:28.401729','2010-11-15 19:43:12.386298','journal//original/2010/11/15/19/41','journal//finded/2010/11/15/19/41',3,NULL,'2010-11-15 19:41:28.434965');
INSERT INTO "videoclient_journal" VALUES(4,NULL,1,35,'2010-11-15 19:44:59.393217','2010-11-15 19:45:29.668841','journal//original/2010/11/15/19/44','journal//finded/2010/11/15/19/44',3,NULL,'2010-11-15 19:44:59.427105');
INSERT INTO "videoclient_journal" VALUES(5,NULL,1,0,'2010-11-15 19:46:13.552223','2010-11-15 19:46:13.552223','journal//original/2010/11/15/19/46','journal//finded/2010/11/15/19/46',3,NULL,'2010-11-15 19:46:13.583875');
INSERT INTO "videoclient_journal" VALUES(6,NULL,1,35,'2010-11-15 19:46:57.009638','2010-11-15 19:47:08.310982','journal//original/2010/11/15/19/46_1','journal//finded/2010/11/15/19/46_1',3,NULL,'2010-11-15 19:46:57.036173');
INSERT INTO "videoclient_journal" VALUES(7,NULL,1,35,'2010-11-15 19:47:51.237445','2010-11-15 19:48:25.048037','journal//original/2010/11/15/19/47','journal//finded/2010/11/15/19/47',3,NULL,'2010-11-15 19:47:51.296091');
INSERT INTO "videoclient_journal" VALUES(8,NULL,1,37,'2010-11-15 19:48:56.438132','2010-11-15 19:49:28.467328','journal//original/2010/11/15/19/48','journal//finded/2010/11/15/19/48',3,NULL,'2010-11-15 19:48:56.465575');
INSERT INTO "videoclient_journal" VALUES(9,NULL,1,37,'2010-11-15 19:51:39.061583','2010-11-15 19:52:20.150750','journal//original/2010/11/15/19/51','journal//finded/2010/11/15/19/51',3,NULL,'2010-11-15 19:51:39.085445');
INSERT INTO "videoclient_journal" VALUES(10,NULL,1,0,'2010-11-15 19:54:06.398579','2010-11-15 19:54:06.398579','journal//original/2010/11/15/19/54','journal//finded/2010/11/15/19/54',3,NULL,'2010-11-15 19:54:06.423365');
INSERT INTO "videoclient_journal" VALUES(11,NULL,2,0,'2010-11-15 19:55:55.597861','2010-11-15 19:56:08.195004','journal//original/2010/11/15/19/55','journal//finded/2010/11/15/19/55',3,NULL,'2010-11-15 19:55:55.630495');
INSERT INTO "videoclient_journal" VALUES(12,NULL,2,0,'2010-11-15 20:04:49.007405','2010-11-15 20:04:49.007405','journal//original/2010/11/15/20/04','journal//finded/2010/11/15/20/04',3,NULL,'2010-11-15 20:04:49.034871');
INSERT INTO "videoclient_journal" VALUES(13,NULL,1,34,'2010-11-15 20:05:19.521948','2010-11-15 20:05:20.657774','journal//original/2010/11/15/20/05','journal//finded/2010/11/15/20/05',3,NULL,'2010-11-15 20:05:19.564787');
INSERT INTO "videoclient_journal" VALUES(14,NULL,2,0,'2010-11-15 20:05:54.188474','2010-11-15 20:05:54.188474','journal//original/2010/11/15/20/05_1','journal//finded/2010/11/15/20/05_1',3,NULL,'2010-11-15 20:05:54.212767');
INSERT INTO "videoclient_journal" VALUES(15,NULL,1,35,'2010-11-15 20:09:08.849406','2010-11-15 20:09:22.824182','journal//original/2010/11/15/20/09','journal//finded/2010/11/15/20/09',3,NULL,'2010-11-15 20:09:08.871634');
INSERT INTO "videoclient_journal" VALUES(16,NULL,1,36,'2010-11-15 20:10:08.888155','2010-11-15 20:10:10.993244','journal//original/2010/11/15/20/10','journal//finded/2010/11/15/20/10',3,NULL,'2010-11-15 20:10:08.911624');
INSERT INTO "videoclient_journal" VALUES(17,NULL,2,0,'2010-11-15 20:11:59.378575','2010-11-15 20:11:59.378575','journal//original/2010/11/15/20/11','journal//finded/2010/11/15/20/11',3,NULL,'2010-11-15 20:11:59.400630');
INSERT INTO "videoclient_journal" VALUES(18,NULL,1,0,'2010-11-15 20:12:55.599735','2010-11-15 20:13:28.767469','journal//original/2010/11/15/20/12','journal//finded/2010/11/15/20/12',3,NULL,'2010-11-15 20:12:55.638002');
INSERT INTO "videoclient_journal" VALUES(19,NULL,2,0,'2010-11-15 20:16:00.077623','2010-11-15 20:16:00.077623','journal//original/2010/11/15/20/16','journal//finded/2010/11/15/20/16',3,NULL,'2010-11-15 20:16:00.107143');
INSERT INTO "videoclient_journal" VALUES(20,NULL,1,36,'2010-11-15 20:16:32.634736','2010-11-15 20:19:29.169697','journal//original/2010/11/15/20/16_1','journal//finded/2010/11/15/20/16_1',3,NULL,'2010-11-15 20:16:32.667721');
INSERT INTO "videoclient_journal" VALUES(21,NULL,1,0,'2010-11-15 20:21:14.218398','2010-11-15 20:21:14.218398','journal//original/2010/11/15/20/21','journal//finded/2010/11/15/20/21',3,NULL,'2010-11-15 20:21:14.249129');
INSERT INTO "videoclient_journal" VALUES(22,NULL,1,0,'2010-11-15 20:21:51.011561','2010-11-15 20:21:51.011561','journal//original/2010/11/15/20/21_1','journal//finded/2010/11/15/20/21_1',3,NULL,'2010-11-15 20:21:51.044007');
INSERT INTO "videoclient_journal" VALUES(23,NULL,1,0,'2010-11-15 20:22:39.813227','2010-11-15 20:22:48.190683','journal//original/2010/11/15/20/22','journal//finded/2010/11/15/20/22',3,NULL,'2010-11-15 20:22:39.837770');
INSERT INTO "videoclient_journal" VALUES(24,NULL,1,36,'2010-11-15 20:23:25.868360','2010-11-15 20:24:19.791939','journal//original/2010/11/15/20/23','journal//finded/2010/11/15/20/23',3,NULL,'2010-11-15 20:23:25.920576');
INSERT INTO "videoclient_journal" VALUES(25,NULL,1,35,'2010-11-15 20:25:03.473026','2010-11-15 20:25:03.473026','journal//original/2010/11/15/20/25','journal//finded/2010/11/15/20/25',3,NULL,'2010-11-15 20:25:03.507536');
INSERT INTO "videoclient_journal" VALUES(26,NULL,1,32,'2010-11-15 20:25:40.879929','2010-11-15 20:25:40.879929','journal//original/2010/11/15/20/25_1','journal//finded/2010/11/15/20/25_1',3,NULL,'2010-11-15 20:25:40.903726');
INSERT INTO "videoclient_journal" VALUES(27,NULL,1,41,'2010-11-15 20:28:10.314531','2010-11-15 20:28:12.542033','journal//original/2010/11/15/20/28','journal//finded/2010/11/15/20/28',3,NULL,'2010-11-15 20:28:10.345171');
INSERT INTO "videoclient_journal" VALUES(28,NULL,1,0,'2010-11-15 20:28:52.602576','2010-11-15 20:29:35.595030','journal//original/2010/11/15/20/28_1','journal//finded/2010/11/15/20/28_1',3,NULL,'2010-11-15 20:28:52.634972');
INSERT INTO "videoclient_journal" VALUES(29,NULL,2,0,'2010-11-15 20:30:37.580399','2010-11-15 20:30:37.580399','journal//original/2010/11/15/20/30','journal//finded/2010/11/15/20/30',3,NULL,'2010-11-15 20:30:37.607397');
INSERT INTO "videoclient_journal" VALUES(30,NULL,2,0,'2010-11-15 20:31:23.453629','2010-11-15 20:31:23.453629','journal//original/2010/11/15/20/31','journal//finded/2010/11/15/20/31',3,NULL,'2010-11-15 20:31:23.483356');
INSERT INTO "videoclient_journal" VALUES(31,NULL,2,0,'2010-11-15 20:32:06.402688','2010-11-15 20:32:06.402688','journal//original/2010/11/15/20/32','journal//finded/2010/11/15/20/32',3,NULL,'2010-11-15 20:32:06.442442');
INSERT INTO "videoclient_journal" VALUES(32,NULL,2,0,'2010-11-15 20:32:48.200221','2010-11-15 20:32:48.200221','journal//original/2010/11/15/20/32_1','journal//finded/2010/11/15/20/32_1',3,NULL,'2010-11-15 20:32:48.229585');
INSERT INTO "videoclient_journal" VALUES(33,NULL,2,35,'2010-11-15 20:35:39.527429','2010-11-15 20:36:15.693356','journal//original/2010/11/15/20/35','journal//finded/2010/11/15/20/35',3,NULL,'2010-11-15 20:35:39.562492');
INSERT INTO "videoclient_journal" VALUES(34,NULL,2,0,'2010-11-15 20:39:43.325319','2010-11-15 20:39:43.325319','journal//original/2010/11/15/20/39','journal//finded/2010/11/15/20/39',3,NULL,'2010-11-15 20:39:43.349368');
INSERT INTO "videoclient_journal" VALUES(35,NULL,1,0,'2010-11-15 20:41:36.111717','2010-11-15 20:41:40.178996','journal//original/2010/11/15/20/41','journal//finded/2010/11/15/20/41',3,NULL,'2010-11-15 20:41:36.191924');
INSERT INTO "videoclient_journal" VALUES(36,NULL,1,35,'2010-11-15 20:42:12.990858','2010-11-15 20:42:12.990858','journal//original/2010/11/15/20/42','journal//finded/2010/11/15/20/42',3,NULL,'2010-11-15 20:42:13.017147');
INSERT INTO "videoclient_journal" VALUES(37,NULL,1,34,'2010-11-15 20:43:01.210500','2010-11-15 20:43:10.494474','journal//original/2010/11/15/20/43','journal//finded/2010/11/15/20/43',3,NULL,'2010-11-15 20:43:01.268868');
INSERT INTO "videoclient_journal" VALUES(38,NULL,1,37,'2010-11-15 20:43:47.708152','2010-11-15 20:45:39.903374','journal//original/2010/11/15/20/43_1','journal//finded/2010/11/15/20/43_1',3,NULL,'2010-11-15 20:43:47.740673');
INSERT INTO "videoclient_journal" VALUES(39,NULL,1,36,'2010-11-15 20:46:14.274125','2010-11-15 20:48:18.700563','journal//original/2010/11/15/20/46','journal//finded/2010/11/15/20/46',3,NULL,'2010-11-15 20:46:14.296420');
INSERT INTO "videoclient_journal" VALUES(40,NULL,1,38,'2010-11-15 20:48:52.925932','2010-11-15 20:49:01.583123','journal//original/2010/11/15/20/48','journal//finded/2010/11/15/20/48',3,NULL,'2010-11-15 20:48:52.961075');
INSERT INTO "videoclient_journal" VALUES(41,NULL,1,0,'2010-11-15 20:49:38.846130','2010-11-15 20:49:38.846130','journal//original/2010/11/15/20/49','journal//finded/2010/11/15/20/49',3,NULL,'2010-11-15 20:49:38.877561');
INSERT INTO "videoclient_journal" VALUES(42,NULL,1,37,'2010-11-15 20:50:24.621318','2010-11-15 20:53:33.453044','journal//original/2010/11/15/20/50','journal//finded/2010/11/15/20/50',3,NULL,'2010-11-15 20:50:24.645282');
INSERT INTO "videoclient_journal" VALUES(43,NULL,1,36,'2010-11-15 20:54:13.082956','2010-11-15 20:55:39.679523','journal//original/2010/11/15/20/54','journal//finded/2010/11/15/20/54',3,NULL,'2010-11-15 20:54:13.105652');
INSERT INTO "videoclient_journal" VALUES(44,NULL,1,36,'2010-11-15 20:56:13.746616','2010-11-15 20:56:58.114864','journal//original/2010/11/15/20/56','journal//finded/2010/11/15/20/56',3,NULL,'2010-11-15 20:56:13.793442');
INSERT INTO "videoclient_journal" VALUES(45,NULL,1,36,'2010-11-15 20:57:30.531073','2010-11-15 21:00:17.903012','journal//original/2010/11/15/20/57','journal//finded/2010/11/15/20/57',3,NULL,'2010-11-15 20:57:30.712041');
INSERT INTO "videoclient_journal" VALUES(46,NULL,1,39,'2010-11-15 21:00:48.849554','2010-11-15 21:00:50.355949','journal//original/2010/11/15/21/00','journal//finded/2010/11/15/21/00',3,NULL,'2010-11-15 21:00:48.889798');
INSERT INTO "videoclient_journal" VALUES(47,NULL,2,0,'2010-11-15 21:01:24.744146','2010-11-15 21:01:24.744146','journal//original/2010/11/15/21/01','journal//finded/2010/11/15/21/01',3,NULL,'2010-11-15 21:01:24.768663');
INSERT INTO "videoclient_journal" VALUES(48,NULL,2,0,'2010-11-15 21:07:32.894587','2010-11-15 21:07:32.894587','journal//original/2010/11/15/21/07','journal//finded/2010/11/15/21/07',3,NULL,'2010-11-15 21:07:32.916499');
INSERT INTO "videoclient_journal" VALUES(49,NULL,1,37,'2010-11-15 21:08:14.265261','2010-11-15 21:09:32.173209','journal//original/2010/11/15/21/08','journal//finded/2010/11/15/21/08',3,NULL,'2010-11-15 21:08:14.295993');
INSERT INTO "videoclient_journal" VALUES(50,NULL,2,36,'2010-11-15 21:10:22.279093','2010-11-15 21:12:15.064245','journal//original/2010/11/15/21/10','journal//finded/2010/11/15/21/10',3,NULL,'2010-11-15 21:10:22.300298');
INSERT INTO "videoclient_journal" VALUES(51,NULL,1,34,'2010-11-15 21:14:16.456760','2010-11-15 21:14:16.972671','journal//original/2010/11/15/21/14','journal//finded/2010/11/15/21/14',3,NULL,'2010-11-15 21:14:16.482715');
INSERT INTO "videoclient_journal" VALUES(52,NULL,1,36,'2010-11-15 21:14:58.191755','2010-11-15 21:16:47.481984','journal//original/2010/11/15/21/14_1','journal//finded/2010/11/15/21/14_1',3,NULL,'2010-11-15 21:14:58.218182');
INSERT INTO "videoclient_journal" VALUES(53,NULL,1,36,'2010-11-15 21:17:30.956154','2010-11-15 21:17:36.403336','journal//original/2010/11/15/21/17','journal//finded/2010/11/15/21/17',3,NULL,'2010-11-15 21:17:30.980607');
INSERT INTO "videoclient_journal" VALUES(54,NULL,2,0,'2010-11-15 21:21:16.867055','2010-11-15 21:21:16.867055','journal//original/2010/11/15/21/21','journal//finded/2010/11/15/21/21',3,NULL,'2010-11-15 21:21:16.895214');
INSERT INTO "videoclient_journal" VALUES(55,NULL,1,0,'2010-11-15 21:24:32.523685','2010-11-15 21:24:32.523685','journal//original/2010/11/15/21/24','journal//finded/2010/11/15/21/24',3,NULL,'2010-11-15 21:24:32.548808');
INSERT INTO "videoclient_journal" VALUES(56,NULL,1,0,'2010-11-15 21:26:02.969784','2010-11-15 21:26:25.582814','journal//original/2010/11/15/21/26','journal//finded/2010/11/15/21/26',3,NULL,'2010-11-15 21:26:02.996387');
INSERT INTO "videoclient_journal" VALUES(57,NULL,1,34,'2010-11-15 21:27:11.396368','2010-11-15 21:28:52.941793','journal//original/2010/11/15/21/27','journal//finded/2010/11/15/21/27',3,NULL,'2010-11-15 21:27:11.423261');
INSERT INTO "videoclient_journal" VALUES(58,NULL,1,34,'2010-11-15 21:29:56.830567','2010-11-15 21:30:34.005079','journal//original/2010/11/15/21/29','journal//finded/2010/11/15/21/29',3,NULL,'2010-11-15 21:29:56.858674');
INSERT INTO "videoclient_journal" VALUES(59,NULL,2,35,'2010-11-15 21:32:44.226973','2010-11-15 21:33:29.866845','journal//original/2010/11/15/21/32','journal//finded/2010/11/15/21/32',3,NULL,'2010-11-15 21:32:44.255619');
INSERT INTO "videoclient_journal" VALUES(60,NULL,2,0,'2010-11-15 21:34:02.870289','2010-11-15 21:34:02.870289','journal//original/2010/11/15/21/34','journal//finded/2010/11/15/21/34',3,NULL,'2010-11-15 21:34:02.900236');
INSERT INTO "videoclient_journal" VALUES(61,NULL,2,0,'2010-11-15 21:37:48.491167','2010-11-15 21:37:48.491167','journal//original/2010/11/15/21/37','journal//finded/2010/11/15/21/37',3,NULL,'2010-11-15 21:37:48.524116');
INSERT INTO "videoclient_journal" VALUES(62,NULL,1,33,'2010-11-15 21:38:37.377072','2010-11-15 21:38:37.972537','journal//original/2010/11/15/21/38','journal//finded/2010/11/15/21/38',3,NULL,'2010-11-15 21:38:37.412483');
INSERT INTO "videoclient_journal" VALUES(63,NULL,2,34,'2010-11-15 21:39:12.861191','2010-11-15 21:41:13.611784','journal//original/2010/11/15/21/39','journal//finded/2010/11/15/21/39',3,NULL,'2010-11-15 21:39:12.890952');
INSERT INTO "videoclient_journal" VALUES(64,NULL,2,0,'2010-11-15 21:42:25.265761','2010-11-15 21:42:25.265761','journal//original/2010/11/15/21/42','journal//finded/2010/11/15/21/42',3,NULL,'2010-11-15 21:42:25.291033');
INSERT INTO "videoclient_journal" VALUES(65,NULL,2,0,'2010-11-15 21:46:29.629986','2010-11-15 21:46:37.452493','journal//original/2010/11/15/21/46','journal//finded/2010/11/15/21/46',3,NULL,'2010-11-15 21:46:29.655589');
INSERT INTO "videoclient_journal" VALUES(66,NULL,2,0,'2010-11-15 21:48:04.671108','2010-11-15 21:48:04.671108','journal//original/2010/11/15/21/48','journal//finded/2010/11/15/21/48',3,NULL,'2010-11-15 21:48:04.708652');
INSERT INTO "videoclient_journal" VALUES(67,NULL,2,0,'2010-11-15 21:50:30.792221','2010-11-15 21:50:30.792221','journal//original/2010/11/15/21/50','journal//finded/2010/11/15/21/50',3,NULL,'2010-11-15 21:50:30.826243');
INSERT INTO "videoclient_journal" VALUES(68,NULL,2,0,'2010-11-15 21:51:43.266668','2010-11-15 21:51:43.266668','journal//original/2010/11/15/21/51','journal//finded/2010/11/15/21/51',3,NULL,'2010-11-15 21:51:43.298850');
INSERT INTO "videoclient_journal" VALUES(69,NULL,2,0,'2010-11-15 21:53:51.810731','2010-11-15 21:54:12.639738','journal//original/2010/11/15/21/53','journal//finded/2010/11/15/21/53',3,NULL,'2010-11-15 21:53:51.842454');
INSERT INTO "videoclient_journal" VALUES(70,NULL,2,0,'2010-11-15 21:54:52.677171','2010-11-15 21:54:52.677171','journal//original/2010/11/15/21/54','journal//finded/2010/11/15/21/54',3,NULL,'2010-11-15 21:54:52.705791');
INSERT INTO "videoclient_journal" VALUES(71,NULL,2,0,'2010-11-15 21:55:39.962343','2010-11-15 21:55:39.962343','journal//original/2010/11/15/21/55','journal//finded/2010/11/15/21/55',3,NULL,'2010-11-15 21:55:39.986082');
INSERT INTO "videoclient_journal" VALUES(72,NULL,1,0,'2010-11-15 21:57:27.231907','2010-11-15 21:57:27.231907','journal//original/2010/11/15/21/57','journal//finded/2010/11/15/21/57',3,NULL,'2010-11-15 21:57:27.256720');
INSERT INTO "videoclient_journal" VALUES(73,NULL,2,0,'2010-11-15 21:58:13.215421','2010-11-15 21:58:13.215421','journal//original/2010/11/15/21/58','journal//finded/2010/11/15/21/58',3,NULL,'2010-11-15 21:58:13.247531');
INSERT INTO "videoclient_journal" VALUES(74,NULL,2,0,'2010-11-15 21:58:44.179650','2010-11-15 21:58:44.179650','journal//original/2010/11/15/21/58_1','journal//finded/2010/11/15/21/58_1',3,NULL,'2010-11-15 21:58:44.221139');
INSERT INTO "videoclient_journal" VALUES(75,NULL,2,0,'2010-11-15 22:03:16.260166','2010-11-15 22:03:16.260166','journal//original/2010/11/15/22/03','journal//finded/2010/11/15/22/03',3,NULL,'2010-11-15 22:03:16.279753');
INSERT INTO "videoclient_journal" VALUES(76,NULL,2,36,'2010-11-15 22:06:56.406169','2010-11-15 22:07:12.535658','journal//original/2010/11/15/22/06','journal//finded/2010/11/15/22/06',3,NULL,'2010-11-15 22:06:56.428309');
INSERT INTO "videoclient_journal" VALUES(77,NULL,2,0,'2010-11-15 22:08:17.060931','2010-11-15 22:08:17.060931','journal//original/2010/11/15/22/08','journal//finded/2010/11/15/22/08',3,NULL,'2010-11-15 22:08:17.095307');
INSERT INTO "videoclient_journal" VALUES(78,NULL,2,0,'2010-11-16 07:59:02.700266','2010-11-16 07:59:05.704926','journal//original/2010/11/16/07/59','journal//finded/2010/11/16/07/59',3,NULL,'2010-11-16 07:59:02.761144');
INSERT INTO "videoclient_journal" VALUES(79,NULL,2,0,'2010-11-16 07:59:59.617899','2010-11-16 08:00:48.096010','journal//original/2010/11/16/07/59_1','journal//finded/2010/11/16/07/59_1',3,NULL,'2010-11-16 07:59:59.653815');
INSERT INTO "videoclient_journal" VALUES(80,NULL,2,0,'2010-11-16 08:01:20.462614','2010-11-16 08:03:15.081345','journal//original/2010/11/16/08/01','journal//finded/2010/11/16/08/01',3,NULL,'2010-11-16 08:01:20.495177');
INSERT INTO "videoclient_journal" VALUES(81,NULL,2,0,'2010-11-16 08:03:52.136312','2010-11-16 08:04:27.013324','journal//original/2010/11/16/08/03','journal//finded/2010/11/16/08/03',3,NULL,'2010-11-16 08:03:52.159348');
INSERT INTO "videoclient_journal" VALUES(82,NULL,2,0,'2010-11-16 08:05:12.442337','2010-11-16 08:05:12.442337','journal//original/2010/11/16/08/05','journal//finded/2010/11/16/08/05',3,NULL,'2010-11-16 08:05:12.464564');
INSERT INTO "videoclient_journal" VALUES(83,NULL,2,0,'2010-11-16 08:06:38.017513','2010-11-16 08:06:38.017513','journal//original/2010/11/16/08/06','journal//finded/2010/11/16/08/06',3,NULL,'2010-11-16 08:06:38.112490');
INSERT INTO "videoclient_journal" VALUES(84,NULL,2,0,'2010-11-16 08:07:13.264370','2010-11-16 08:07:32.940029','journal//original/2010/11/16/08/07','journal//finded/2010/11/16/08/07',3,NULL,'2010-11-16 08:07:13.293683');
INSERT INTO "videoclient_journal" VALUES(85,NULL,2,0,'2010-11-16 08:08:08.653395','2010-11-16 08:08:34.164412','journal//original/2010/11/16/08/08','journal//finded/2010/11/16/08/08',3,NULL,'2010-11-16 08:08:08.687581');
INSERT INTO "videoclient_journal" VALUES(86,NULL,2,0,'2010-11-16 08:09:16.005991','2010-11-16 08:09:28.746540','journal//original/2010/11/16/08/09','journal//finded/2010/11/16/08/09',3,NULL,'2010-11-16 08:09:16.038311');
INSERT INTO "videoclient_journal" VALUES(87,NULL,2,0,'2010-11-16 08:10:09.041797','2010-11-16 08:11:23.143435','journal//original/2010/11/16/08/10','journal//finded/2010/11/16/08/10',3,NULL,'2010-11-16 08:10:09.069855');
INSERT INTO "videoclient_journal" VALUES(88,NULL,2,0,'2010-11-16 08:12:17.266268','2010-11-16 08:12:18.836198','journal//original/2010/11/16/08/12','journal//finded/2010/11/16/08/12',3,NULL,'2010-11-16 08:12:17.303507');
INSERT INTO "videoclient_journal" VALUES(89,NULL,2,0,'2010-11-16 08:13:03.329371','2010-11-16 08:13:03.329371','journal//original/2010/11/16/08/13','journal//finded/2010/11/16/08/13',3,NULL,'2010-11-16 08:13:03.356672');
INSERT INTO "videoclient_journal" VALUES(90,NULL,2,0,'2010-11-16 08:13:57.050246','2010-11-16 08:14:43.689766','journal//original/2010/11/16/08/13_1','journal//finded/2010/11/16/08/13_1',3,NULL,'2010-11-16 08:13:57.081824');
INSERT INTO "videoclient_journal" VALUES(91,NULL,2,0,'2010-11-16 08:17:17.412731','2010-11-16 08:17:17.412731','journal//original/2010/11/16/08/17','journal//finded/2010/11/16/08/17',3,NULL,'2010-11-16 08:17:17.447062');
INSERT INTO "videoclient_journal" VALUES(92,NULL,2,0,'2010-11-16 08:17:59.132950','2010-11-16 08:19:49.046584','journal//original/2010/11/16/08/17_1','journal//finded/2010/11/16/08/17_1',3,NULL,'2010-11-16 08:17:59.166168');
INSERT INTO "videoclient_journal" VALUES(93,NULL,2,0,'2010-11-16 08:20:57.754072','2010-11-16 08:22:57.309140','journal//original/2010/11/16/08/20','journal//finded/2010/11/16/08/20',3,NULL,'2010-11-16 08:20:57.784651');
INSERT INTO "videoclient_journal" VALUES(94,NULL,2,0,'2010-11-16 08:24:09.191663','2010-11-16 08:24:09.191663','journal//original/2010/11/16/08/24','journal//finded/2010/11/16/08/24',3,NULL,'2010-11-16 08:24:09.224642');
INSERT INTO "videoclient_journal" VALUES(95,NULL,2,0,'2010-11-16 08:24:56.070087','2010-11-16 08:25:16.217782','journal//original/2010/11/16/08/24_1','journal//finded/2010/11/16/08/24_1',3,NULL,'2010-11-16 08:24:56.101669');
INSERT INTO "videoclient_journal" VALUES(96,NULL,2,0,'2010-11-16 08:26:08.627866','2010-11-16 08:26:08.627866','journal//original/2010/11/16/08/26','journal//finded/2010/11/16/08/26',3,NULL,'2010-11-16 08:26:08.659453');
INSERT INTO "videoclient_journal" VALUES(97,NULL,2,0,'2010-11-16 08:26:57.471775','2010-11-16 08:27:30.424071','journal//original/2010/11/16/08/26_1','journal//finded/2010/11/16/08/26_1',3,NULL,'2010-11-16 08:26:57.494344');
INSERT INTO "videoclient_journal" VALUES(98,NULL,2,0,'2010-11-16 08:28:01.536918','2010-11-16 08:28:09.769472','journal//original/2010/11/16/08/28','journal//finded/2010/11/16/08/28',3,NULL,'2010-11-16 08:28:01.571122');
INSERT INTO "videoclient_journal" VALUES(99,NULL,2,0,'2010-11-16 08:29:03.836738','2010-11-16 08:29:14.883904','journal//original/2010/11/16/08/29','journal//finded/2010/11/16/08/29',3,NULL,'2010-11-16 08:29:03.866413');
INSERT INTO "videoclient_journal" VALUES(100,NULL,2,0,'2010-11-16 08:29:56.716760','2010-11-16 08:29:58.200840','journal//original/2010/11/16/08/29_1','journal//finded/2010/11/16/08/29_1',3,NULL,'2010-11-16 08:29:56.749989');
INSERT INTO "videoclient_journal" VALUES(101,NULL,2,0,'2010-11-16 08:30:58.004497','2010-11-16 08:30:58.004497','journal//original/2010/11/16/08/30','journal//finded/2010/11/16/08/30',3,NULL,'2010-11-16 08:30:58.040137');
INSERT INTO "videoclient_journal" VALUES(102,NULL,2,0,'2010-11-16 08:32:43.080760','2010-11-16 08:33:23.229516','journal//original/2010/11/16/08/32','journal//finded/2010/11/16/08/32',3,NULL,'2010-11-16 08:32:43.100773');
INSERT INTO "videoclient_journal" VALUES(103,NULL,2,0,'2010-11-16 08:35:06.643286','2010-11-16 08:35:06.643286','journal//original/2010/11/16/08/35','journal//finded/2010/11/16/08/35',3,NULL,'2010-11-16 08:35:06.691115');
INSERT INTO "videoclient_journal" VALUES(104,NULL,2,0,'2010-11-16 08:35:59.774665','2010-11-16 08:36:28.223762','journal//original/2010/11/16/08/35_1','journal//finded/2010/11/16/08/35_1',3,NULL,'2010-11-16 08:35:59.796575');
INSERT INTO "videoclient_journal" VALUES(105,NULL,2,0,'2010-11-16 08:38:25.132426','2010-11-16 08:38:25.132426','journal//original/2010/11/16/08/38','journal//finded/2010/11/16/08/38',3,NULL,'2010-11-16 08:38:25.163184');
INSERT INTO "videoclient_journal" VALUES(106,NULL,2,0,'2010-11-16 08:39:18.923975','2010-11-16 08:40:03.781093','journal//original/2010/11/16/08/39','journal//finded/2010/11/16/08/39',3,NULL,'2010-11-16 08:39:18.953966');
INSERT INTO "videoclient_journal" VALUES(107,NULL,2,0,'2010-11-16 08:41:49.851217','2010-11-16 08:42:04.756871','journal//original/2010/11/16/08/41','journal//finded/2010/11/16/08/41',3,NULL,'2010-11-16 08:41:49.873913');
INSERT INTO "videoclient_journal" VALUES(108,NULL,2,0,'2010-11-16 08:46:00.987133','2010-11-16 08:46:07.427222','journal//original/2010/11/16/08/46','journal//finded/2010/11/16/08/46',3,NULL,'2010-11-16 08:46:01.008225');
INSERT INTO "videoclient_journal" VALUES(109,NULL,2,0,'2010-11-16 08:47:06.714153','2010-11-16 08:47:13.370319','journal//original/2010/11/16/08/47','journal//finded/2010/11/16/08/47',3,NULL,'2010-11-16 08:47:06.796878');
INSERT INTO "videoclient_journal" VALUES(110,NULL,2,0,'2010-11-16 08:48:31.089737','2010-11-16 08:49:49.683081','journal//original/2010/11/16/08/48','journal//finded/2010/11/16/08/48',3,NULL,'2010-11-16 08:48:31.148483');
INSERT INTO "videoclient_journal" VALUES(111,NULL,2,0,'2010-11-16 08:50:58.580711','2010-11-16 08:51:27.891639','journal//original/2010/11/16/08/50','journal//finded/2010/11/16/08/50',3,NULL,'2010-11-16 08:50:58.712238');
INSERT INTO "videoclient_journal" VALUES(112,NULL,2,0,'2010-11-16 08:54:10.130529','2010-11-16 08:54:38.273217','journal//original/2010/11/16/08/54','journal//finded/2010/11/16/08/54',3,NULL,'2010-11-16 08:54:10.152634');
INSERT INTO "videoclient_journal" VALUES(113,NULL,2,0,'2010-11-16 08:55:17.606294','2010-11-16 08:55:56.328058','journal//original/2010/11/16/08/55','journal//finded/2010/11/16/08/55',3,NULL,'2010-11-16 08:55:17.706267');
INSERT INTO "videoclient_journal" VALUES(114,NULL,2,0,'2010-11-16 08:56:36.349417','2010-11-16 08:57:02.541668','journal//original/2010/11/16/08/56','journal//finded/2010/11/16/08/56',3,NULL,'2010-11-16 08:56:36.375639');
INSERT INTO "videoclient_journal" VALUES(115,NULL,2,0,'2010-11-16 08:57:46.699500','2010-11-16 08:57:46.699500','journal//original/2010/11/16/08/57','journal//finded/2010/11/16/08/57',3,NULL,'2010-11-16 08:57:46.865587');
INSERT INTO "videoclient_journal" VALUES(116,NULL,2,0,'2010-11-16 09:00:21.966219','2010-11-16 09:00:21.966219','journal//original/2010/11/16/09/00','journal//finded/2010/11/16/09/00',3,NULL,'2010-11-16 09:00:22.066562');
INSERT INTO "videoclient_journal" VALUES(117,NULL,2,0,'2010-11-16 09:01:34.100315','2010-11-16 09:02:23.454892','journal//original/2010/11/16/09/01','journal//finded/2010/11/16/09/01',3,NULL,'2010-11-16 09:01:34.126775');
INSERT INTO "videoclient_journal" VALUES(118,NULL,2,0,'2010-11-16 09:04:23.631001','2010-11-16 09:04:23.631001','journal//original/2010/11/16/09/04','journal//finded/2010/11/16/09/04',3,NULL,'2010-11-16 09:04:23.659963');
INSERT INTO "videoclient_journal" VALUES(119,NULL,2,0,'2010-11-16 09:04:57.243889','2010-11-16 09:05:39.274910','journal//original/2010/11/16/09/04_1','journal//finded/2010/11/16/09/04_1',3,NULL,'2010-11-16 09:04:57.278333');
INSERT INTO "videoclient_journal" VALUES(120,NULL,2,0,'2010-11-16 09:07:12.025534','2010-11-16 09:07:58.330627','journal//original/2010/11/16/09/07','journal//finded/2010/11/16/09/07',3,NULL,'2010-11-16 09:07:12.051737');
INSERT INTO "videoclient_journal" VALUES(121,NULL,2,0,'2010-11-16 09:09:35.615453','2010-11-16 09:10:29.442540','journal//original/2010/11/16/09/09','journal//finded/2010/11/16/09/09',3,NULL,'2010-11-16 09:09:35.638016');
INSERT INTO "videoclient_journal" VALUES(122,NULL,2,0,'2010-11-16 09:12:54.248775','2010-11-16 09:13:23.140102','journal//original/2010/11/16/09/12','journal//finded/2010/11/16/09/12',3,NULL,'2010-11-16 09:12:54.278197');
INSERT INTO "videoclient_journal" VALUES(123,NULL,2,0,'2010-11-16 09:15:22.874391','2010-11-16 09:15:22.874391','journal//original/2010/11/16/09/15','journal//finded/2010/11/16/09/15',3,NULL,'2010-11-16 09:15:22.904179');
INSERT INTO "videoclient_journal" VALUES(124,NULL,2,0,'2010-11-16 09:16:34.536149','2010-11-16 09:16:59.302432','journal//original/2010/11/16/09/16','journal//finded/2010/11/16/09/16',3,NULL,'2010-11-16 09:16:34.562771');
INSERT INTO "videoclient_journal" VALUES(125,NULL,2,0,'2010-11-16 09:17:32.776580','2010-11-16 09:19:01.388602','journal//original/2010/11/16/09/17','journal//finded/2010/11/16/09/17',3,NULL,'2010-11-16 09:17:32.798893');
INSERT INTO "videoclient_journal" VALUES(126,NULL,2,0,'2010-11-16 09:22:03.874549','2010-11-16 09:22:03.874549','journal//original/2010/11/16/09/22','journal//finded/2010/11/16/09/22',3,NULL,'2010-11-16 09:22:03.901523');
INSERT INTO "videoclient_journal" VALUES(127,NULL,2,0,'2010-11-16 09:26:14.887918','2010-11-16 09:27:11.694443','journal//original/2010/11/16/09/26','journal//finded/2010/11/16/09/26',3,NULL,'2010-11-16 09:26:14.921531');
INSERT INTO "videoclient_journal" VALUES(128,NULL,2,0,'2010-11-16 09:28:10.618446','2010-11-16 09:28:10.618446','journal//original/2010/11/16/09/28','journal//finded/2010/11/16/09/28',3,NULL,'2010-11-16 09:28:10.660813');
INSERT INTO "videoclient_journal" VALUES(129,NULL,2,0,'2010-11-16 09:29:38.975563','2010-11-16 09:29:38.975563','journal//original/2010/11/16/09/29','journal//finded/2010/11/16/09/29',3,NULL,'2010-11-16 09:29:39.100109');
INSERT INTO "videoclient_journal" VALUES(130,NULL,2,0,'2010-11-16 09:32:09.708692','2010-11-16 09:32:09.708692','journal//original/2010/11/16/09/32','journal//finded/2010/11/16/09/32',3,NULL,'2010-11-16 09:32:09.733815');
INSERT INTO "videoclient_journal" VALUES(131,NULL,2,0,'2010-11-16 09:35:42.350011','2010-11-16 09:35:42.350011','journal//original/2010/11/16/09/35','journal//finded/2010/11/16/09/35',3,NULL,'2010-11-16 09:35:42.373021');
INSERT INTO "videoclient_journal" VALUES(132,NULL,2,0,'2010-11-16 09:36:25.643431','2010-11-16 09:36:25.643431','journal//original/2010/11/16/09/36','journal//finded/2010/11/16/09/36',3,NULL,'2010-11-16 09:36:25.663718');
INSERT INTO "videoclient_journal" VALUES(133,NULL,2,0,'2010-11-16 09:37:32.484663','2010-11-16 09:37:32.484663','journal//original/2010/11/16/09/37','journal//finded/2010/11/16/09/37',3,NULL,'2010-11-16 09:37:32.516628');
INSERT INTO "videoclient_journal" VALUES(134,NULL,2,0,'2010-11-16 09:38:18.665147','2010-11-16 09:38:18.665147','journal//original/2010/11/16/09/38','journal//finded/2010/11/16/09/38',3,NULL,'2010-11-16 09:38:18.692426');
INSERT INTO "videoclient_journal" VALUES(135,NULL,2,0,'2010-11-16 09:39:32.192520','2010-11-16 09:39:32.192520','journal//original/2010/11/16/09/39','journal//finded/2010/11/16/09/39',3,NULL,'2010-11-16 09:39:32.210970');
INSERT INTO "videoclient_journal" VALUES(136,NULL,2,0,'2010-11-16 09:40:54.062545','2010-11-16 09:41:30.879483','journal//original/2010/11/16/09/40','journal//finded/2010/11/16/09/40',3,NULL,'2010-11-16 09:40:54.140622');
INSERT INTO "videoclient_journal" VALUES(137,NULL,2,0,'2010-11-16 09:45:18.700269','2010-11-16 09:45:20.219585','journal//original/2010/11/16/09/45','journal//finded/2010/11/16/09/45',3,NULL,'2010-11-16 09:45:18.752606');
INSERT INTO "videoclient_journal" VALUES(138,NULL,2,0,'2010-11-16 09:47:05.859846','2010-11-16 09:47:29.271515','journal//original/2010/11/16/09/47','journal//finded/2010/11/16/09/47',3,NULL,'2010-11-16 09:47:05.879279');
INSERT INTO "videoclient_journal" VALUES(139,NULL,2,0,'2010-11-16 09:49:20.350686','2010-11-16 09:49:24.577480','journal//original/2010/11/16/09/49','journal//finded/2010/11/16/09/49',3,NULL,'2010-11-16 09:49:20.388088');
INSERT INTO "videoclient_journal" VALUES(140,NULL,2,0,'2010-11-16 09:50:59.176494','2010-11-16 09:50:59.176494','journal//original/2010/11/16/09/50','journal//finded/2010/11/16/09/50',3,NULL,'2010-11-16 09:50:59.207462');
INSERT INTO "videoclient_journal" VALUES(141,NULL,2,0,'2010-11-16 09:52:02.348194','2010-11-16 09:52:16.091596','journal//original/2010/11/16/09/52','journal//finded/2010/11/16/09/52',3,NULL,'2010-11-16 09:52:02.402497');
INSERT INTO "videoclient_journal" VALUES(142,NULL,2,0,'2010-11-16 09:55:39.795381','2010-11-16 09:56:06.197142','journal//original/2010/11/16/09/55','journal//finded/2010/11/16/09/55',3,NULL,'2010-11-16 09:55:39.829773');
INSERT INTO "videoclient_journal" VALUES(143,NULL,2,0,'2010-11-16 09:59:45.488191','2010-11-16 09:59:49.454021','journal//original/2010/11/16/09/59','journal//finded/2010/11/16/09/59',3,NULL,'2010-11-16 09:59:45.535420');
INSERT INTO "videoclient_journal" VALUES(144,NULL,2,0,'2010-11-16 10:01:54.946855','2010-11-16 10:02:24.220002','journal//original/2010/11/16/10/01','journal//finded/2010/11/16/10/01',3,NULL,'2010-11-16 10:01:55.043416');
INSERT INTO "videoclient_journal" VALUES(145,NULL,2,0,'2010-11-16 10:03:37.385254','2010-11-16 10:03:44.966866','journal//original/2010/11/16/10/03','journal//finded/2010/11/16/10/03',3,NULL,'2010-11-16 10:03:37.406445');
INSERT INTO "videoclient_journal" VALUES(146,NULL,2,0,'2010-11-16 10:05:59.133309','2010-11-16 10:05:59.133309','journal//original/2010/11/16/10/05','journal//finded/2010/11/16/10/05',3,NULL,'2010-11-16 10:05:59.210197');
INSERT INTO "videoclient_journal" VALUES(147,NULL,2,0,'2010-11-16 10:09:31.435701','2010-11-16 10:09:31.435701','journal//original/2010/11/16/10/09','journal//finded/2010/11/16/10/09',3,NULL,'2010-11-16 10:09:31.463244');
INSERT INTO "videoclient_journal" VALUES(148,NULL,2,0,'2010-11-16 10:11:53.805470','2010-11-16 10:12:08.955265','journal//original/2010/11/16/10/11','journal//finded/2010/11/16/10/11',3,NULL,'2010-11-16 10:11:53.830603');
INSERT INTO "videoclient_journal" VALUES(149,NULL,2,0,'2010-11-16 10:12:57.528790','2010-11-16 10:13:17.136469','journal//original/2010/11/16/10/12','journal//finded/2010/11/16/10/12',3,NULL,'2010-11-16 10:12:57.559594');
INSERT INTO "videoclient_journal" VALUES(150,NULL,2,0,'2010-11-16 10:15:15.035042','2010-11-16 10:15:15.035042','journal//original/2010/11/16/10/15','journal//finded/2010/11/16/10/15',3,NULL,'2010-11-16 10:15:15.055212');
INSERT INTO "videoclient_journal" VALUES(151,NULL,2,0,'2010-11-16 10:18:42.743240','2010-11-16 10:18:55.501902','journal//original/2010/11/16/10/18','journal//finded/2010/11/16/10/18',3,NULL,'2010-11-16 10:18:42.761133');
INSERT INTO "videoclient_journal" VALUES(152,NULL,2,0,'2010-11-16 10:20:13.881546','2010-11-16 10:20:13.881546','journal//original/2010/11/16/10/20','journal//finded/2010/11/16/10/20',3,NULL,'2010-11-16 10:20:13.903156');
INSERT INTO "videoclient_journal" VALUES(153,NULL,2,0,'2010-11-16 10:20:58.040355','2010-11-16 10:21:22.303822','journal//original/2010/11/16/10/20_1','journal//finded/2010/11/16/10/20_1',3,NULL,'2010-11-16 10:20:58.068664');
INSERT INTO "videoclient_journal" VALUES(154,NULL,2,0,'2010-11-16 10:22:25.828582','2010-11-16 10:22:25.828582','journal//original/2010/11/16/10/22','journal//finded/2010/11/16/10/22',3,NULL,'2010-11-16 10:22:25.853230');
INSERT INTO "videoclient_journal" VALUES(155,NULL,2,0,'2010-11-16 10:23:22.637035','2010-11-16 10:23:22.637035','journal//original/2010/11/16/10/23','journal//finded/2010/11/16/10/23',3,NULL,'2010-11-16 10:23:22.665974');
INSERT INTO "videoclient_journal" VALUES(156,NULL,2,0,'2010-11-16 10:24:35.594568','2010-11-16 10:24:35.594568','journal//original/2010/11/16/10/24','journal//finded/2010/11/16/10/24',3,NULL,'2010-11-16 10:24:35.625538');
INSERT INTO "videoclient_journal" VALUES(157,NULL,2,0,'2010-11-16 10:25:15.361528','2010-11-16 10:25:15.361528','journal//original/2010/11/16/10/25','journal//finded/2010/11/16/10/25',3,NULL,'2010-11-16 10:25:15.387627');
INSERT INTO "videoclient_journal" VALUES(158,NULL,2,0,'2010-11-16 10:27:43.397038','2010-11-16 10:27:43.397038','journal//original/2010/11/16/10/27','journal//finded/2010/11/16/10/27',3,NULL,'2010-11-16 10:27:43.463535');
INSERT INTO "videoclient_journal" VALUES(159,NULL,2,0,'2010-11-16 10:28:23.605969','2010-11-16 10:28:23.605969','journal//original/2010/11/16/10/28','journal//finded/2010/11/16/10/28',3,NULL,'2010-11-16 10:28:23.634227');
INSERT INTO "videoclient_journal" VALUES(160,NULL,2,0,'2010-11-16 10:30:19.971868','2010-11-16 10:30:19.971868','journal//original/2010/11/16/10/30','journal//finded/2010/11/16/10/30',3,NULL,'2010-11-16 10:30:20.018684');
INSERT INTO "videoclient_journal" VALUES(161,NULL,2,0,'2010-11-16 10:33:52.540415','2010-11-16 10:33:52.540415','journal//original/2010/11/16/10/33','journal//finded/2010/11/16/10/33',3,NULL,'2010-11-16 10:33:52.559056');
INSERT INTO "videoclient_journal" VALUES(162,NULL,2,0,'2010-11-16 10:34:48.429837','2010-11-16 10:34:48.429837','journal//original/2010/11/16/10/34','journal//finded/2010/11/16/10/34',3,NULL,'2010-11-16 10:34:48.474896');
INSERT INTO "videoclient_journal" VALUES(163,NULL,2,0,'2010-11-16 10:35:45.253045','2010-11-16 10:35:45.253045','journal//original/2010/11/16/10/35','journal//finded/2010/11/16/10/35',3,NULL,'2010-11-16 10:35:45.350015');
INSERT INTO "videoclient_journal" VALUES(164,NULL,2,0,'2010-11-16 10:38:23.535572','2010-11-16 10:38:23.535572','journal//original/2010/11/16/10/38','journal//finded/2010/11/16/10/38',3,NULL,'2010-11-16 10:38:23.567110');
INSERT INTO "videoclient_journal" VALUES(165,NULL,2,0,'2010-11-16 10:42:08.104066','2010-11-16 10:42:08.104066','journal//original/2010/11/16/10/42','journal//finded/2010/11/16/10/42',3,NULL,'2010-11-16 10:42:08.127289');
INSERT INTO "videoclient_journal" VALUES(166,NULL,2,0,'2010-11-16 10:42:42.612206','2010-11-16 10:42:42.612206','journal//original/2010/11/16/10/42_1','journal//finded/2010/11/16/10/42_1',3,NULL,'2010-11-16 10:42:42.643917');
INSERT INTO "videoclient_journal" VALUES(167,NULL,2,0,'2010-11-16 10:44:45.640105','2010-11-16 10:44:45.640105','journal//original/2010/11/16/10/44','journal//finded/2010/11/16/10/44',3,NULL,'2010-11-16 10:44:45.671107');
INSERT INTO "videoclient_journal" VALUES(168,NULL,2,0,'2010-11-16 10:46:41.709820','2010-11-16 10:46:41.709820','journal//original/2010/11/16/10/46','journal//finded/2010/11/16/10/46',3,NULL,'2010-11-16 10:46:41.740399');
INSERT INTO "videoclient_journal" VALUES(169,NULL,2,0,'2010-11-16 10:49:39.973621','2010-11-16 10:49:39.973621','journal//original/2010/11/16/10/49','journal//finded/2010/11/16/10/49',3,NULL,'2010-11-16 10:49:40.002884');
INSERT INTO "videoclient_journal" VALUES(170,NULL,2,0,'2010-11-16 10:50:10.457576','2010-11-16 10:50:10.457576','journal//original/2010/11/16/10/50','journal//finded/2010/11/16/10/50',3,NULL,'2010-11-16 10:50:10.489330');
INSERT INTO "videoclient_journal" VALUES(171,NULL,2,0,'2010-11-16 10:52:14.415997','2010-11-16 10:52:14.415997','journal//original/2010/11/16/10/52','journal//finded/2010/11/16/10/52',3,NULL,'2010-11-16 10:52:14.450788');
INSERT INTO "videoclient_journal" VALUES(172,NULL,2,0,'2010-11-16 10:55:01.187022','2010-11-16 10:55:01.187022','journal//original/2010/11/16/10/55','journal//finded/2010/11/16/10/55',3,NULL,'2010-11-16 10:55:01.218932');
INSERT INTO "videoclient_journal" VALUES(173,NULL,2,0,'2010-11-16 10:57:58.489832','2010-11-16 10:58:28.054798','journal//original/2010/11/16/10/57','journal//finded/2010/11/16/10/57',3,NULL,'2010-11-16 10:57:58.523313');
INSERT INTO "videoclient_journal" VALUES(174,NULL,2,0,'2010-11-16 10:59:19.083515','2010-11-16 10:59:19.083515','journal//original/2010/11/16/10/59','journal//finded/2010/11/16/10/59',3,NULL,'2010-11-16 10:59:19.113589');
INSERT INTO "videoclient_journal" VALUES(175,NULL,2,0,'2010-11-16 11:00:14.921394','2010-11-16 11:00:14.921394','journal//original/2010/11/16/11/00','journal//finded/2010/11/16/11/00',3,NULL,'2010-11-16 11:00:14.993538');
INSERT INTO "videoclient_journal" VALUES(176,NULL,2,0,'2010-11-16 11:00:47.930037','2010-11-16 11:01:11.433751','journal//original/2010/11/16/11/00_1','journal//finded/2010/11/16/11/00_1',3,NULL,'2010-11-16 11:00:48.017673');
INSERT INTO "videoclient_journal" VALUES(177,NULL,2,0,'2010-11-16 11:02:58.567053','2010-11-16 11:03:25.292805','journal//original/2010/11/16/11/02','journal//finded/2010/11/16/11/02',3,NULL,'2010-11-16 11:02:58.588701');
INSERT INTO "videoclient_journal" VALUES(178,NULL,1,36,'2010-11-16 11:05:08.313523','2010-11-16 11:06:06.668346','journal//original/2010/11/16/11/05','journal//finded/2010/11/16/11/05',3,NULL,'2010-11-16 11:05:08.368418');
INSERT INTO "videoclient_journal" VALUES(179,NULL,2,36,'2010-11-16 11:07:07.601302','2010-11-16 11:08:28.727129','journal//original/2010/11/16/11/07','journal//finded/2010/11/16/11/07',3,NULL,'2010-11-16 11:07:07.629356');
INSERT INTO "videoclient_journal" VALUES(180,NULL,2,0,'2010-11-16 11:09:29.474595','2010-11-16 11:09:29.474595','journal//original/2010/11/16/11/09','journal//finded/2010/11/16/11/09',3,NULL,'2010-11-16 11:09:29.495796');
INSERT INTO "videoclient_journal" VALUES(181,NULL,1,35,'2010-11-16 11:11:23.528532','2010-11-16 11:11:23.528532','journal//original/2010/11/16/11/11','journal//finded/2010/11/16/11/11',3,NULL,'2010-11-16 11:11:23.556947');
INSERT INTO "videoclient_journal" VALUES(182,NULL,2,0,'2010-11-16 11:15:03.634680','2010-11-16 11:15:19.852355','journal//original/2010/11/16/11/15','journal//finded/2010/11/16/11/15',3,NULL,'2010-11-16 11:15:03.658959');
INSERT INTO "videoclient_journal" VALUES(183,NULL,2,0,'2010-11-16 11:16:01.302469','2010-11-16 11:16:17.664640','journal//original/2010/11/16/11/16','journal//finded/2010/11/16/11/16',3,NULL,'2010-11-16 11:16:01.327859');
INSERT INTO "videoclient_journal" VALUES(184,NULL,2,0,'2010-11-16 11:16:48.236589','2010-11-16 11:17:13.004955','journal//original/2010/11/16/11/16_1','journal//finded/2010/11/16/11/16_1',3,NULL,'2010-11-16 11:16:48.260711');
INSERT INTO "videoclient_journal" VALUES(185,NULL,2,0,'2010-11-16 11:17:51.616160','2010-11-16 11:18:04.713277','journal//original/2010/11/16/11/17','journal//finded/2010/11/16/11/17',3,NULL,'2010-11-16 11:17:51.648246');
INSERT INTO "videoclient_journal" VALUES(186,NULL,2,34,'2010-11-16 11:19:08.162452','2010-11-16 11:19:10.923431','journal//original/2010/11/16/11/19','journal//finded/2010/11/16/11/19',3,NULL,'2010-11-16 11:19:08.189315');
INSERT INTO "videoclient_journal" VALUES(187,NULL,1,37,'2010-11-16 11:20:30.930675','2010-11-16 11:21:32.286197','journal//original/2010/11/16/11/20','journal//finded/2010/11/16/11/20',3,NULL,'2010-11-16 11:20:30.997406');
INSERT INTO "videoclient_journal" VALUES(188,NULL,2,34,'2010-11-16 11:22:48.429874','2010-11-16 11:24:58.463517','journal//original/2010/11/16/11/22','journal//finded/2010/11/16/11/22',3,NULL,'2010-11-16 11:22:48.458118');
INSERT INTO "videoclient_journal" VALUES(189,NULL,1,0,'2010-11-16 11:25:34.222723','2010-11-16 11:25:34.222723','journal//original/2010/11/16/11/25','journal//finded/2010/11/16/11/25',3,NULL,'2010-11-16 11:25:34.252080');
INSERT INTO "videoclient_journal" VALUES(190,NULL,1,34,'2010-11-16 11:26:09.610839','2010-11-16 11:28:29.587873','journal//original/2010/11/16/11/26','journal//finded/2010/11/16/11/26',3,NULL,'2010-11-16 11:26:09.635596');
INSERT INTO "videoclient_journal" VALUES(191,NULL,1,0,'2010-11-16 11:29:18.239919','2010-11-16 11:29:51.059509','journal//original/2010/11/16/11/29','journal//finded/2010/11/16/11/29',3,NULL,'2010-11-16 11:29:18.268424');
INSERT INTO "videoclient_journal" VALUES(192,NULL,1,35,'2010-11-16 11:30:23.261489','2010-11-16 11:32:21.666099','journal//original/2010/11/16/11/30','journal//finded/2010/11/16/11/30',3,NULL,'2010-11-16 11:30:23.377570');
INSERT INTO "videoclient_journal" VALUES(193,NULL,1,0,'2010-11-16 11:33:00.758066','2010-11-16 11:33:00.758066','journal//original/2010/11/16/11/33','journal//finded/2010/11/16/11/33',3,NULL,'2010-11-16 11:33:00.870837');
INSERT INTO "videoclient_journal" VALUES(194,NULL,1,0,'2010-11-16 11:33:48.299155','2010-11-16 11:34:06.417617','journal//original/2010/11/16/11/33_1','journal//finded/2010/11/16/11/33_1',3,NULL,'2010-11-16 11:33:48.329287');
INSERT INTO "videoclient_journal" VALUES(195,NULL,1,34,'2010-11-16 11:34:41.578805','2010-11-16 11:35:56.857525','journal//original/2010/11/16/11/34','journal//finded/2010/11/16/11/34',3,NULL,'2010-11-16 11:34:41.603930');
INSERT INTO "videoclient_journal" VALUES(196,NULL,1,0,'2010-11-16 11:36:38.197453','2010-11-16 11:37:12.565136','journal//original/2010/11/16/11/36','journal//finded/2010/11/16/11/36',3,NULL,'2010-11-16 11:36:38.220538');
INSERT INTO "videoclient_journal" VALUES(197,NULL,2,0,'2010-11-16 11:38:00.041139','2010-11-16 11:38:00.041139','journal//original/2010/11/16/11/38','journal//finded/2010/11/16/11/38',3,NULL,'2010-11-16 11:38:00.079023');
CREATE INDEX "auth_permission_e4470c6e" ON "auth_permission" ("content_type_id");
CREATE INDEX "auth_group_permissions_bda51c3c" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_1e014c8f" ON "auth_group_permissions" ("permission_id");
CREATE INDEX "auth_user_user_permissions_fbfc09f1" ON "auth_user_user_permissions" ("user_id");
CREATE INDEX "auth_user_user_permissions_1e014c8f" ON "auth_user_user_permissions" ("permission_id");
CREATE INDEX "auth_user_groups_fbfc09f1" ON "auth_user_groups" ("user_id");
CREATE INDEX "auth_user_groups_bda51c3c" ON "auth_user_groups" ("group_id");
CREATE INDEX "auth_message_fbfc09f1" ON "auth_message" ("user_id");
CREATE INDEX "videoclient_translation_bda51c3c" ON "videoclient_translation" ("group_id");
CREATE INDEX "videoclient_translation_7ab48146" ON "videoclient_translation" ("language_id");
CREATE INDEX "django_admin_log_fbfc09f1" ON "django_admin_log" ("user_id");
CREATE INDEX "django_admin_log_e4470c6e" ON "django_admin_log" ("content_type_id");
CREATE INDEX "videoclient_positionuser_8034cb5d" ON "videoclient_positionuser" ("division_id");
CREATE INDEX "videoclient_statususer_8034cb5d" ON "videoclient_statususer" ("division_id");
CREATE INDEX "videoclient_user_8034cb5d" ON "videoclient_user" ("division_id");
CREATE INDEX "videoclient_user_80180135" ON "videoclient_user" ("position_id");
CREATE INDEX "videoclient_user_44224078" ON "videoclient_user" ("status_id");
CREATE INDEX "videoclient_user_8aa0f76c" ON "videoclient_user" ("kpp_id");
CREATE INDEX "videoclient_loginjournal_fbfc09f1" ON "videoclient_loginjournal" ("user_id");
CREATE INDEX "videoclient_person_fbfc09f1" ON "videoclient_person" ("user_id");
CREATE INDEX "videoclient_person_bda51c3c" ON "videoclient_person" ("group_id");
CREATE INDEX "videoclient_person_44224078" ON "videoclient_person" ("status_id");
CREATE INDEX "videoclient_person_f4226d13" ON "videoclient_person" ("document_id");
CREATE INDEX "videoclient_person_42dc49bc" ON "videoclient_person" ("category_id");
CREATE INDEX "videoclient_personid_21b911c5" ON "videoclient_personid" ("person_id");
CREATE INDEX "videoclient_rulegroup_bda51c3c" ON "videoclient_rulegroup" ("group_id");
CREATE INDEX "videoclient_rulegroup_1c671d36" ON "videoclient_rulegroup" ("rule_id");
CREATE INDEX "videoclient_camera_8aa0f76c" ON "videoclient_camera" ("kpp_id");
CREATE INDEX "videoclient_visitingcard_e4fc0429" ON "videoclient_visitingcard" ("visitor_id");
CREATE INDEX "videoclient_visitingcard_21b911c5" ON "videoclient_visitingcard" ("person_id");
CREATE INDEX "videoclient_visitingcard_c0bae6b9" ON "videoclient_visitingcard" ("ground_id");
CREATE INDEX "videoclient_journal_21b911c5" ON "videoclient_journal" ("person_id");
CREATE INDEX "videoclient_journal_ed2c9bb" ON "videoclient_journal" ("camera_id");
CREATE INDEX "videoclient_journal_c4bf4a4f" ON "videoclient_journal" ("positions_status_id");
CREATE INDEX "videoclient_journal_4198106c" ON "videoclient_journal" ("operator_id");
COMMIT;

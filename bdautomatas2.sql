-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: automatas2
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(25) COLLATE utf8mb4_general_ci NOT NULL,
  `apellidoP` varchar(25) COLLATE utf8mb4_general_ci NOT NULL,
  `apellidoM` varchar(25) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'Cindy','Martinez','Sanchez'),(2,'Sofia','Martinez','Sanchez'),(3,'Maria','Lopez','Gomez'),(4,'Ana','Rodriguez','Martinez'),(5,'Luis','Garcia','Sanchez'),(6,'Carlos','Ramirez','Hernandez');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id_p` int NOT NULL AUTO_INCREMENT,
  `codBarras` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `nombre` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `cantidad` int NOT NULL,
  `proveedores` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `especificaciones` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `fechaCad` date NOT NULL,
  `costoCompra` int NOT NULL,
  `costoVenta` int NOT NULL,
  PRIMARY KEY (`id_p`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'123','Barritas',30,'Barcel','Barritas de piña','2024-10-28',12,23),(2,'258','sabritas',12,'sabritas','100g','2024-10-23',15,24),(3,'789','Jabón',34,'Ace','1 kg','2024-12-19',28,45),(4,'456','Refresco fanta',34,'Cocacola','500 ml','2024-11-20',12,24),(5,'369','Refresco sprite',24,'Cocacola','500 ml','2024-11-19',12,25),(6,'453','jugo boing',40,'boing','100 ml','2024-02-02',13,25);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_u` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `ap` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `am` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `clave` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
  `telefono` int NOT NULL,
  `correo` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `contras` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_u`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'madelene','hernandez','vargas','21isc013',2147483647,'madelene@gmail.com','Taylorswift13#'),(8,'Brandon','Smith','Johnson','21isc035',452678913,'brandon@gmail.com','BrandonSmith22#'),(9,'Camila','Gómez','López','21isc036',461789234,'camila@gmail.com','CamilaGomez33#'),(10,'Diego','Hernández','Martínez','21isc037',459876541,'diego@gmail.com','DiegoHdz44#'),(11,'Emily','Taylor','Brown','21isc038',457123986,'emily@gmail.com','EmilyTaylor55#'),(12,'Fernando','Díaz','Pérez','21isc039',453678902,'fernando@gmail.com','FernandoDiaz66#'),(13,'alison','Swift','Alwyn','21isc034',458693712,'alison@gmail.com','Alisonswift11#'),(14,'Brandon','Smith','Johnson','21isc035',452678913,'brandon@gmail.com','BrandonSmith22#'),(15,'Camila','Gómez','López','21isc036',461789234,'camila@gmail.com','CamilaGomez33#'),(16,'Diego','Hernández','Martínez','21isc037',459876541,'diego@gmail.com','DiegoHdz44#'),(17,'Emily','Taylor','Brown','21isc038',457123986,'emily@gmail.com','EmilyTaylor55#'),(18,'Fernando','Díaz','Pérez','21isc039',453678902,'fernando@gmail.com','FernandoDiaz66#'),(19,'Brandon','Smith','Johnson','21isc035',452678913,'brandon@gmail.com','BrandonSmith22#'),(20,'Camila','Gómez','López','21isc036',461789234,'camila@gmail.com','CamilaGomez33#'),(21,'Diego','Hernández','Martínez','21isc037',459876541,'diego@gmail.com','DiegoHdz44#'),(22,'Emily','Taylor','Brown','21isc038',457123986,'emily@gmail.com','EmilyTaylor55#'),(23,'Fernando','Díaz','Pérez','21isc039',453678902,'fernando@gmail.com','FernandoDiaz66#');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `id_venta` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `nombreU` varchar(30) COLLATE utf8mb4_general_ci NOT NULL,
  `cliente` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `productos` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `cantidadP` int NOT NULL,
  `total` float NOT NULL,
  `efectivo` float NOT NULL,
  `cambio` float NOT NULL,
  `tipoPago` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_venta`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (1,'2024-11-06 23:39:44','1','2','',0,0,0,0,''),(16,'2024-11-07 00:13:55','1','2','',0,0,0,0,''),(17,'2024-11-07 06:28:17','madelene','2','Refresco sprite (x1)',1,25,0,-25,'0'),(18,'2024-11-07 06:31:02','madelene','1','Barritas (x1)',1,23,0,-23,'0'),(19,'2024-11-07 08:12:05','madelene','1','Refresco sprite (x1), Refresco sprite (x1)',2,50,0,-50,'0'),(20,'2024-11-07 08:19:38','madelene','1','Barritas (x1)',1,23,100,77,'0'),(21,'2024-11-07 08:26:04','madelene','1','Refresco sprite (x1)',1,25,100,75,'0'),(22,'2024-11-07 08:31:17','madelene','1','sabritas (x1)',1,24,50,26,'0'),(23,'2024-11-07 08:35:12','madelene','1','Refresco sprite (x1)',1,25,200,175,'0'),(24,'2024-11-07 08:40:35','madelene','2','Barritas (x1)',1,23,100,77,'0'),(25,'2024-11-07 08:45:41','madelene','1','sabritas (x1)',1,24,100,76,'0'),(26,'2024-11-07 09:25:26','madelene','1','Barritas (x1)',1,23,50,27,'0'),(27,'2024-11-07 09:41:27','madelene','2','Barritas (x1)',1,23,50,27,'0'),(28,'2024-11-07 09:58:40','madelene','1','sabritas (x1)',1,24,50,26,'0'),(29,'2024-11-07 10:49:35','madelene','Cindy Martinez Sanchez','Barritas (x1)',1,23,50,27,'0'),(30,'2024-11-07 11:47:34','madelene','Sofia Martinez Sanchez','sabritas (x1)',1,24,50,26,'0'),(31,'2024-11-07 12:20:30','madelene','Cindy Martinez Sanchez','Barritas (x1)',1,23,50,27,'0'),(32,'2024-11-07 12:30:03','madelene','Cindy Martinez Sanchez','Refresco sprite (x1)',1,25,100,75,'0'),(33,'2024-09-22 10:00:00','madelene','Sofia Martinez Sanchez','sabritas (x1), sabritas (x1)',2,48,100,52,'0'),(34,'2024-10-02 10:00:00','madelene','1','[{\"nombre\":\"Barritas\",\"precio\":23,\"cantidad\":1}]',1,23,100,77,'efectivo'),(35,'2024-11-08 00:00:00','madelene','1','[{\"nombre\":\"Barritas\",\"precio\":23,\"cantidad\":1}]',1,23,100,77,'efectivo'),(36,'2024-11-13 00:00:00','madelene','1','[{\"nombre\":\"Refresco sprite\",\"precio\":25,\"cantidad\":3}]',1,75,100,25,'efectivo'),(37,'2024-05-01 11:00:00','madelene','Sofia Martinez Sanchez','Barritas, Refresco sprite, Jabón',8,252,500,248,'Efectivo'),(38,'2024-11-13 18:08:04','madelene','Cindy Martinez Sanchez','[[\"123\", \"Barritas\", \"23\", \"5\", \"115.0\"], [\"369\", \"Refresco sprite\", \"25\", \"3\", \"75.0\"]]',2,209,0,0,'Tarjeta'),(39,'2024-11-28 00:00:00','madelene','Cindy Martinez Sanchez','Barritas, Refresco sprite',2,48,200,152,'Efectivo'),(40,'2024-12-02 00:00:00','madelene','Sofia Martinez Sanchez','Barritas, Refresco sprite',4,94,200,106,'Efectivo'),(41,'2024-12-02 00:00:00','alison','Ana Rodriguez Martinez','Refresco sprite, jugo boing',4,100,200,100,'Efectivo');
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'automatas2'
--
/*!50003 DROP PROCEDURE IF EXISTS `FiltrarVentas` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `FiltrarVentas`(
    IN D INT,            -- Día del mes (1-31)
    IN M VARCHAR(15),    -- Nombre del mes (e.g., "Enero")
    IN S INT,            -- Semana (número de semana del año)
    IN empleado VARCHAR(50) -- Nombre del empleado
)
BEGIN
SET lc_time_names = 'es_ES';

IF D IS NOT NULL AND M IS NULL AND S IS NULL AND empleado IS NULL THEN
		SELECT id_venta, fecha, nombreU, cliente, productos, total, tipoPago FROM ventas WHERE DAY(fecha) = D;
    ELSEIF D IS NULL AND M IS NOT NULL AND S IS NULL AND empleado IS NULL THEN
		SELECT id_venta, fecha, nombreU, cliente, productos, total, tipoPago FROM ventas  WHERE MONTHNAME(fecha) = M;
	ELSEIF D IS NULL AND M IS NULL AND S IS NOT NULL AND empleado IS NULL THEN
		SELECT id_venta, fecha, nombreU, cliente, productos, total, tipoPago FROM ventas WHERE WEEK(fecha, 1) = S;
	ELSEIF D IS NULL AND M IS NULL AND S IS NULL AND empleado IS NOT NULL THEN
		SELECT id_venta, fecha, nombreU, cliente, productos, total, tipoPago FROM ventas WHERE nombreU = empleado;
        
	ELSEIF D IS NOT NULL AND M IS NOT NULL AND S IS NULL AND empleado IS NULL THEN
		SELECT id_venta, fecha, nombreU, cliente, productos, total, tipoPago FROM ventas WHERE DAY(fecha) = D AND MONTHNAME(fecha) = M;
	ELSEIF D IS NOT NULL AND M IS NOT NULL AND S IS NULL AND empleado IS NOT NULL THEN
		SELECT id_venta, fecha, nombreU, cliente, productos, total, tipoPago FROM ventas WHERE DAY(fecha) = D AND MONTHNAME(fecha) = M AND nombreU = empleado;
	ELSEIF D IS NULL AND M IS NULL AND S IS NOT NULL AND empleado IS NOT NULL THEN
		SELECT id_venta, fecha, nombreU, cliente, productos, total, tipoPago FROM ventas WHERE WEEK(fecha, 1) = S AND nombreU = empleado;
	else
		SELECT 'FILTRO NO VALIDO' as Mensaje;
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-02 19:22:51

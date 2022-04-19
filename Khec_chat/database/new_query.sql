-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 12, 2022 at 07:32 PM
-- Server version: 10.1.40-MariaDB
-- PHP Version: 7.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `chatbot_query`
--

-- --------------------------------------------------------

--
-- Table structure for table `new_query`
--

CREATE TABLE `new_query` (
  `S.N` int(10) NOT NULL,
  `Query` text NOT NULL,
  `freq` int(11) NOT NULL DEFAULT '1',
  `Entry_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `new_query`
--

INSERT INTO `new_query` (`S.N`, `Query`, `freq`, `Entry_at`) VALUES
(1, 'Rose is red', 1, '2021-10-21 08:52:31'),
(3, 'green color', 1, '2021-10-21 09:09:55'),
(9, 'white house', 1, '0000-00-00 00:00:00'),
(10, 'red house', 1, '2021-10-21 10:00:13'),
(11, 'red panda', 1, '2021-10-21 10:01:03'),
(12, 'red panda', 1, '2021-10-21 10:01:43'),
(14, 'sky is blue', 1, '2021-10-21 10:08:01'),
(15, 'what is features?', 1, '2021-10-28 05:50:30'),
(17, 'tell me about location', 1, '2022-01-22 14:47:41'),
(18, 'tell location', 1, '2022-01-22 14:47:56'),
(19, 'can you tell me location', 1, '2022-01-22 14:58:02'),
(20, 'can you tell me your location please?', 1, '2022-01-22 15:28:41'),
(21, 'tell location?', 1, '2022-01-22 15:28:53'),
(22, 'phone no', 1, '2022-01-22 15:34:27'),
(23, 'phone no.', 1, '2022-01-22 15:34:40'),
(24, 'can you tell me your location please?', 1, '2022-01-22 15:44:11'),
(29, 'phone no.', 1, '2022-01-22 16:20:29'),
(30, 'phone', 1, '2022-01-22 16:21:02'),
(31, 'can you give me location?', 1, '2022-01-22 16:50:48'),
(33, 'can you tell me acanteen?', 1, '2022-01-23 03:20:02'),
(34, 'what services do you rovide?', 1, '2022-01-23 03:46:32'),
(35, 'what services do you p\nrovide?', 1, '2022-01-23 03:46:54'),
(36, 'who', 1, '2022-01-23 04:04:58'),
(37, 'is that tasty?', 1, '2022-01-23 04:06:37'),
(38, 'is there any councselling?', 1, '2022-01-23 04:11:39'),
(39, 'is there any coun\nselling?', 1, '2022-01-23 04:11:55'),
(40, 'is there any coun\nselling?', 1, '2022-01-23 04:12:03'),
(41, 'how about practicals', 1, '2022-01-23 04:13:09'),
(42, 'is park', 1, '2022-01-23 07:37:36'),
(43, 'is there availability of bike park?', 1, '2022-01-23 07:38:19'),
(44, 'can i wear?', 1, '2022-01-23 07:54:06'),
(45, 'can you locates me to your college?', 1, '2022-01-23 07:55:02'),
(47, 'you fool', 1, '2022-01-23 08:01:21'),
(48, 'how can i join the bachleor in architecture', 1, '2022-01-23 12:19:01'),
(49, 'what subjects do you teach?', 1, '2022-01-23 12:34:28'),
(50, 'which faculty are available here?', 1, '2022-01-23 12:35:31'),
(51, 'faculty?', 1, '2022-01-23 12:49:36'),
(52, 'can you tell me locat?', 1, '2022-01-28 12:34:42'),
(53, 'can you tell me place of khec?', 1, '2022-01-29 12:26:25'),
(54, 'how can i reach there?', 1, '2022-01-29 12:27:32'),
(55, 'how to reach there?', 1, '2022-01-29 13:43:20'),
(56, 'how can i reach there?', 1, '2022-01-29 13:43:35'),
(57, 'how can i reach there?', 1, '2022-01-29 13:53:47'),
(58, 'how to reach there?', 1, '2022-01-29 13:57:47'),
(59, 'how can i reach there?', 1, '2022-01-29 13:58:10'),
(68, 'can you send the shift', 1, '2022-02-12 14:50:28'),
(69, 'shift', 1, '2022-02-12 14:54:02'),
(70, 'what is the schedule of classes', 1, '2022-02-12 16:02:11'),
(71, 'how are seats are available of b.tech', 1, '2022-02-12 16:05:55'),
(72, 'when did computer engineering finished?', 1, '2022-02-12 18:11:29'),
(73, 'when did computer engineering completed?', 1, '2022-02-12 18:18:18'),
(74, 'sss', 3, '2022-02-12 18:28:40');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `new_query`
--
ALTER TABLE `new_query`
  ADD PRIMARY KEY (`S.N`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `new_query`
--
ALTER TABLE `new_query`
  MODIFY `S.N` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=75;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

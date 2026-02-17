-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 17, 2026 at 11:17 AM
-- Server version: 9.3.0
-- PHP Version: 8.5.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `alfiyah_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `hashed_password` varchar(255) NOT NULL,
  `role` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `address`, `phone_number`, `hashed_password`, `role`) VALUES
(1, 'Admin User', 'admin@gmail.com', 'Admin Address', '081234567890', '$2b$12$LWJpBoQ.M4yXiefiMkgkNuzdSvLYLWqls/vVz/xLZir8VHkliuV4S', 'admin'),
(2, 'wais', 'wais@gmail.com', 'makassar', NULL, '$2b$12$JCdHA4WF6nGowXgJEZH9qOQyUN72s2XV8zj.MtqozZNHKR20Agg6G', 'customer'),
(3, 'wais2', 'wais2@gmail.com', 'makassar', NULL, '$2b$12$XcQwhR.SPdWo4Dg0lx6EOeDZKxFncIDH7TYZlx4PzSR17PbeNJhxm', 'customer'),
(4, 'uhuyy', 'uhuy@gmail.com', 'uhuyy', '09712635526222', '$2b$12$IJUNC4GdFySGWF4et4XHeuRoRXTzlQ.5MRRPJVYX2GzSezyd2toyy', 'customer'),
(5, 'Kiki', 'kiki@gmail.com', 'Makassar', '08616253736', '$2b$12$LlmDHh51QwiaqpOR0l/ymeFhuLPERM3DlaGtHmHVTDH/zktgWPSSm', 'customer'),
(6, 'Lia', 'lia@gmail.com', 'Toddopuli', '084762068833', '$2b$12$RP18cLVA5PYhjhE5xlGzr.logekrvts/RbLmmYAysYM.MoK21JLoe', 'customer'),
(7, 'Atikah', 'atikah@gmail.com', 'Btp', '089375811253', '$2b$12$gQPnT73RqYG.3VMy7C5EBevNoWEJ0x99INKfbrjVm400qjiImWoQG', 'customer'),
(8, 'Putri', 'putri@gmail.com', 'Borong', '082185238019', '$2b$12$XyCmFu29g6ijvrdol1koKeiUfffFGd3FAGCOxCuygaOk7tzhvk.qS', 'customer'),
(9, 'Kia', 'kia@gmail.com', 'Baruga', '083628474610', '$2b$12$viiHY.BYeJRXp/WOXR4GUelEN7nZf6QAqXcmerlhOY0UpexuPF2Di', 'customer'),
(10, 'Intan', 'intan@gmail.com', 'Tamalate', '089121429500', '$2b$12$apBCa0M9Js3wSQ.46cV1WOrXrbdjy8FIQSMyKl2Yti1z5k8clqjE2', 'customer'),
(11, 'Unay', 'unay@gmail.com', 'Panakukang', '083341633882', '$2b$12$4SUgtp1MgrKIYEdDzPqj9.CCxOmJ.l8dqNkhk0GX.B0s2cvBiaRtu', 'customer'),
(12, 'Setiara', 'setiara@gmail.com', 'Ratulangi', '089608336158', '$2b$12$/4p70X2fU.b1LbG58PyFR.K8zqqGHSjilANG8AbiRkom9mBhG8Ks.', 'customer'),
(13, 'Faradila', 'faradila@gmail.com', 'A.Mappaoddang', '088070497676', '$2b$12$0X4Z80RlhJ9eRPmTLDHa0eu/v5OvrSMk.pJ6SKg1RJOOWy3olyLoS', 'customer'),
(14, 'Nailah', 'nailah@gmail.com', 'A.Mappaoddang', '089214193031', '$2b$12$KEDdWlZEsY6Km672u8PdrOCk7Y.vHaPlxIlxaTgSGmtV0fNkfkD7W', 'customer'),
(15, 'Wanda', 'wanda@gmail.com', 'Landak lama', '088555533373', '$2b$12$E.Z0oyL4XIM/W6W4lZ2PfO5qCQ/.ljI/Fe.zsd.XJwokBNv3SvEpm', 'customer'),
(16, 'Seri', 'seri@gmail.com', 'Perintis', '089424022998', '$2b$12$g6muFergfe4dSqjMVxE1hO/13Xj7RFxZn3Q6NljZbpySyaF1TTVY.', 'customer'),
(17, 'Setiara', 'setiara1@gmail.com', 'BTP', '083180882286', '$2b$12$1vrnmXrVDJgs96ZrxEHbvuUMoygXAvHHaa9IcuyrV6xvncFXo236i', 'customer'),
(18, 'Faradila', 'faradila1@gmail.com', 'A.Mappaoddang', '085101673347', '$2b$12$kCOpdVWS4H.lDhZZkKwLsel0EVZOiFyAnp82vubX6GnYW5.p9V8Me', 'customer'),
(19, 'Nailah', 'nailah1@gmail.com', 'A.Mappaoddang', '081443963980', '$2b$12$Fdzg4oBBPqDKgmH2d8Jz2eeeWnUEaP46MEoqQeO47H6h9adItlJqe', 'customer'),
(20, 'Zelvi', 'zelvi@gmail.com', 'Onta lama', '086222852821', '$2b$12$5.bdCfrLUQvp1PDCQa6ymODn1GWRNMj2bbXVbd22oCQ5s5tO0dtmK', 'customer'),
(21, 'Mutmainna', 'mutmainna@gmail.com', 'cendrawasih', '085650991719', '$2b$12$QTP7UZi0DlEHcZVl8SfRs.vmrFDygwHc6TpoAc9xqNOzEU3nrNnZO', 'customer'),
(22, 'Wanda', 'wanda1@gmail.com', 'Landak lama', '082835504953', '$2b$12$9Ayu.QU6iLGmrOueJxwO0.8Iy.fP4.0i2SwIWDH0VIIA29ZgYkyUK', 'customer'),
(23, 'Revalina', 'revalina@gmail.com', 'Alauddin', '083318641288', '$2b$12$i14gmo0sAs3ENi/5VwRwAeqJUUxf5fqxrET00HuVtZT1IJ2HtYb6G', 'customer'),
(24, 'Angriani', 'angriani@gmail.com', 'Toddopuli', '080062114937', '$2b$12$EaWC0GY2Po2BKpkR03pwi.p99kqa822CBYVVg3.y5mCjOKRhNUif2', 'customer'),
(25, 'Lisa', 'lisa@gmail.com', 'Rappocini', '088406732813', '$2b$12$Pzp/pYsxEhKddWZVoq1TSOqeuD3k8lYQA8beVZk2Icn5ecj01W5gm', 'customer'),
(26, 'Nur', 'nur@gmail.com', 'Andi djemma', '088685181409', '$2b$12$xlzvBkRgqwLVk5Tg8Xu.yuoa3UaNUSVsiaIvRez48u7zmCMAqQBo6', 'customer'),
(27, 'Putri', 'putri1@gmail.com', 'Tidung', '080488367692', '$2b$12$sEDtC8oxvKnXb.kezjOU2u1krX9t3UiMqJxerWsPCoaW2xNNe7pMG', 'customer'),
(28, 'Nurul', 'nurul@gmail.com', 'Hertasning', '086422187368', '$2b$12$YdlvHxqy3CkM2oU9SYZxG.xXbFBJZfLgp0360Cea0hNqah/rQ/ByC', 'customer'),
(29, 'Sulis', 'sulis@gmail.com', 'Royal spring', '086418128229', '$2b$12$QNIn9L5Cd.VSqeoLK1aJ4OLeR6INmzIK1wSs8CFPAsMjwFkdiTO8m', 'customer'),
(30, 'Nhursya', 'nhursya@gmail.com', 'Perumnas antang', '080071461445', '$2b$12$4HDWl5eWIiOpgEe4emvj3eLMPmTm7zMVCw.gnmLIStmfRXNctaima', 'customer'),
(31, 'Riningta', 'riningta@gmail.com', 'Alauddin', '087620175390', '$2b$12$cafBSiHLqoLFbMnjiSZSpeyKtzXbvyVjQhQ6wOtEYPS9UHgASLEjq', 'customer'),
(32, 'Ayhu', 'ayhu@gmail.com', 'Antang', '087123194388', '$2b$12$M8eup5GwGTO/kAElPSLT7ePL5HenHWaHLVZ.5H8zhEM1nS77i4m/W', 'customer'),
(33, 'Faika', 'faika@gmail.com', 'Hertasning', '081421190372', '$2b$12$F8ltWfZiPdb3tzPf0S9YnufZit3AuqdC2kyDlpxD10NXtb0b/KGNC', 'customer'),
(34, 'Andi idar', 'andi.idar@gmail.com', 'Tamalate', '089290388584', '$2b$12$jtYXhwSX1Z7z26lSifeu9uaONnrivfQwmxcxwy3mKz/KjjdNxv4R2', 'customer'),
(35, 'Dewi', 'dewi@gmail.com', 'Hertasning', '086231167343', '$2b$12$R9uRMm11R3ax8Aq/qCNGnehtf9iV.4vuX3HRxyDwVBhyHSAcirz7.', 'customer'),
(36, 'Lisa', 'lisa1@gmail.com', 'Pendidikan', '089984467956', '$2b$12$NZ3DG97TigZPhmiXCf45cOF7Kp9eOSD7mBkGY.oNK78zc/tWHDh3W', 'customer'),
(37, 'Safirah', 'safirah@gmail.com', 'Pendidikan', '086080861261', '$2b$12$iz1vWXBQeWKyC7/g5oEDaOC8/83UAoN7wkF08h5Sm69Rm/U2HI0Ee', 'customer'),
(38, 'Azirah', 'azirah@gmail.com', 'Tidung', '088931000352', '$2b$12$ztTwNK8txui2fSzwPAZmMuVS3B06eZL/77CHrUf/NHaeBQzPgAiza', 'customer'),
(39, 'Anhy', 'anhy@gmail.com', 'Tamalate', '081078310245', '$2b$12$vcDOU21KH/FW7CytK.CMHet3hPmLZdlHuBxkwPv41FXJ0pYbOUeQK', 'customer'),
(40, 'Dewi', 'dewi1@gmail.com', 'Tamalate', '086898419599', '$2b$12$SsaIahuaiSZW6E6S5ROanuzXr4nshenwt0UVJTr7ixF9LKvuDazvu', 'customer'),
(41, 'Eka', 'eka@gmail.com', 'Boulevard', '080644958376', '$2b$12$czQCNrMy0DTdysi6YmeyL.qUhgHHm3kmUF8H0xNPIQ1VJAfsXzPDm', 'customer'),
(42, 'Fadiah', 'fadiah@gmail.com', 'Boulevard', '087641243565', '$2b$12$Shyafpxp1VqOSXOrm/JjJOkaxNOrgJsVLPnUCab9GdJ5h7vuTT1he', 'customer'),
(43, 'Khaerani', 'khaerani@gmail.com', 'Pettarani', '082063710703', '$2b$12$DGPYqfxgIrlEGkwgqiA96uCQI3XGPf/iSJzZX57s1nSxKatAiIKt2', 'customer'),
(44, 'Patta', 'patta@gmail.com', 'Pettarani', '086530313087', '$2b$12$A8n93a8FJG4NRePCm1uR3uE/sCqoV/OWjdpR.56dnx.ftuyn3fVfC', 'customer'),
(45, 'Safirah', 'safirah1@gmail.com', 'Pettarani', '081715770293', '$2b$12$ug77l6wdvnQkH6GhCchWy.C1JivoYxSoyEkybl2WYL0UhyEc42JIO', 'customer'),
(46, 'yuly', 'yuly@gmail.com', 'Pettarani', '086939499617', '$2b$12$S0CumCMonKIgpIpBu3MvxO9Cs5ZGeMLmBHVaBmkxC2puZ.KMqM.4m', 'customer'),
(47, 'Nunu', 'nunu@gmail.com', 'Pettarani', '083685713631', '$2b$12$.Cz6HeQZz8UnTomZV0QMbOeW6gDw8Irg8XgUirx6cy8qWFbr4l5mC', 'customer'),
(48, 'Andriany', 'andriany@gmail.com', 'Pettarani', '080682264728', '$2b$12$ysfli2.fAbLp6gqqu3.VR.dq8OofFBZmLip1zmhRecpdv.8yBIMAu', 'customer'),
(49, 'Andi indar', 'andi.indar@gmail.com', 'Pettarani', '084415590090', '$2b$12$yW.YOc16E5fygWDLOXkij.3NCWZ7sfIE1/OJ/42tooITwKzaE67q6', 'customer'),
(50, 'Lisa', 'lisa2@gmail.com', 'Pettarani', '082523570999', '$2b$12$JlK2lw9PX7vO/X.nXbn1xuX4AmxAkqBq6fJJ65sLz/KhJETYEbjFu', 'customer'),
(51, 'Sasa', 'sasa@gmail.com', 'Pettarani', '085966892896', '$2b$12$6lbdnVVzmuIRnnc28qQpQOhCZyrrE3KAVE30D/I.l.O9T107Doy.C', 'customer'),
(52, 'Arnita', 'arnita@gmail.com', 'Pettarani', '089757255367', '$2b$12$1CReWNVjlXICihKTx0xE1ucdDgQoa9e..pR17dV92paYNQlDgxhs2', 'customer'),
(53, 'Intan', 'intan1@gmail.com', 'Pettarani', '084482708071', '$2b$12$hiQzmkIqLL7AYoa06nSg5eJbrRLHuUG9aeGDFsZqF8MkCchHBFFNG', 'customer'),
(54, 'Azirah', 'azirah1@gmail.com', 'Pettarani', '080949340327', '$2b$12$ZgzbJXgTz78d4rsNztDFQuOjfnNijusbrC/FgG0LSm0cxOGzQYvdC', 'customer'),
(55, 'Putri', 'putri2@gmail.com', 'Abdesir', '089015897595', '$2b$12$ZFBpVtch602BANNFSqj0r.6H0a.mElENFYWHniM/pVI53VcILerYG', 'customer'),
(56, 'Indah', 'indah@gmail.com', 'Btp', '082048406292', '$2b$12$McLWvigVBbR6uAgRtjFpFeZhiKT.H7EgmDVQIVYLSfmqktFxi.GgK', 'customer'),
(57, 'Alya', 'alya@gmail.com', 'Moncongloe', '080009297240', '$2b$12$YJL1o6rHjMrpcJbN8VwzjuMxSmmiwQK8RZ0Ysh6tiUASoH7Au9dyu', 'customer'),
(58, 'Adillah', 'adillah@gmail.com', 'Moncongloe', '088521632629', '$2b$12$39JCCnxMeZJC8gCKhEZWC.T8dm1ubAc8dOAuDih/f8tu.XQr0uinG', 'customer'),
(59, 'Almaida', 'almaida@gmail.com', 'Btp', '089439866440', '$2b$12$Wa.7RjuPoaWuYsICyATb1Os84MyO9V2c1G2/OUmsSei49mJhzzpXK', 'customer'),
(60, 'Citra', 'citra@gmail.com', 'Perintis', '084691888129', '$2b$12$P4VQSLraSmsJpB.MJY1PzObgPoMk1pLH4WGQ.E4cxJvxorxbNEguO', 'customer'),
(61, 'Auliaa', 'auliaa@gmail.com', 'Pettarani', '085548430969', '$2b$12$qk9lSaVqlB5CArQQHqRgN.GU.DTs2wLCnXID84MZOCpLF0NEzqylK', 'customer'),
(62, 'Atikah', 'atikah1@gmail.com', 'Talasalapang', '087450279184', '$2b$12$w9M4/Os5MSCfV1pLrqJ2nOBcwAVKewhAk/U36mTl1.mkldlhnk/ca', 'customer'),
(63, 'Devy', 'devy@gmail.com', 'Pongtiku', '082253159074', '$2b$12$HFxGunDbmBRqWInf9PIxo.hY2Le5nq2UzgZsE7L7E4v07iqlSsYI2', 'customer'),
(64, 'Mustika', 'mustika@gmail.com', 'Pendidikan', '080693349777', '$2b$12$1kyhp/9YRTQuA..too90w.IyjmFE9chNvKgjBNRkbQE6QscrPWbKC', 'customer'),
(65, 'Ardiana', 'ardiana@gmail.com', 'Majene', '084428493922', '$2b$12$9oVXeBFCiSSk9uarsoE0ROG0bddIiTJbNuodaqWjS.ExkZZmyVoWy', 'customer'),
(66, 'Dilla', 'dilla@gmail.com', 'Majene', '089221328700', '$2b$12$/5QT3XYScuBHSzPnXZL9leaR.q9LfXnKc44jXi214y2ER6te5lLH6', 'customer'),
(67, 'Husna', 'husna@gmail.com', 'Majene', '080857207134', '$2b$12$m6cmWe4WhFYNNagf605wp.x9bmw5Q4y.ppBQ93FAJRTnE/k.fRa1y', 'customer'),
(68, 'Maimuna', 'maimuna@gmail.com', 'Majene', '087099945094', '$2b$12$3/5sR6XMBWl4C21sS2bZ8ei/pJsZJHt.TNcEHIVbB/zc7p6dFMO9a', 'customer'),
(69, 'Mardianti', 'mardianti@gmail.com', 'Majene', '089465352302', '$2b$12$wp4.TB3rLcb/NQDKLm3BlOwzrxJ.VVQiNoXH2pGcJstgWHYSt9ddW', 'customer'),
(70, 'Khalisa', 'khalisa@gmail.com', 'Antang', '084827127840', '$2b$12$eTdBvoj8V84MQgK4roxoS.jJ2AJq9/Sejkuj3kWzpCJxTH8tqcB26', 'customer'),
(71, 'Adinda', 'adinda@gmail.com', 'Rajawali', '083684628933', '$2b$12$DZb3AAnC6X1UxbWJgvaC/.VzlZGn6qQUjtODPweSY8ucMzQsd.16y', 'customer'),
(72, 'Mega', 'mega@gmail.com', 'Rajawali', '087986297366', '$2b$12$vKdOf2UaIQx2b4jmTPohdOb8kDlADikAdZqAGidxXBxsfU.9ZbZvu', 'customer'),
(73, 'Aisyah', 'aisyah@gmail.com', 'Rajawali', '084634257326', '$2b$12$lzMgguEi3LGGqT37//zHPedVXqHZ7I2v.w.mF5urFrJDVQOgqHeFO', 'customer'),
(74, 'Manda', 'manda@gmail.com', 'Rajawali', '087716615562', '$2b$12$3RrzEiEL1nkQORi6DF0u1exIjyZ05Ard8q0yxY0YSPHMwLK0upQGm', 'customer'),
(75, 'Putri', 'putri3@gmail.com', 'Rajawali', '088985078040', '$2b$12$VvZrbweHIaUJ54LW2WA2wOU8AwU85Wm/dRTI9b184sKzrZ7Em2snq', 'customer'),
(76, 'Resky', 'resky@gmail.com', 'Rajawali', '084560568580', '$2b$12$UM/Z1U734OkQGdprZOcNs.YxwUeNJqAq3TIm4qbQu9HuU1AXygPVm', 'customer'),
(77, 'Fitri', 'fitri@gmail.com', 'Pettarani', '084524070726', '$2b$12$qDjSQHOJgcyr2aVbsRGlc.EsMI4ghufbY4BsKNNV8RFei8olRnuqa', 'customer'),
(78, 'Kiki', 'kiki1@gmail.com', 'Landak', '089617947602', '$2b$12$CWLOMltLH.79h7IGR6JIjuS9QtTkpFuzsDkv.8qppwlpFqshgsaoi', 'customer'),
(79, 'Pauziah', 'pauziah@gmail.com', 'Rappocini', '084083588331', '$2b$12$ApWEwO48SwcTUtMRSiy1tOl8gNtP1ztNl3a2H4lbpvHgY32lIDHg.', 'customer'),
(80, 'Ersa', 'ersa@gmail.com', 'Rajawali', '085683745071', '$2b$12$WtxWrWKoSGSJPwYIXG5fGOQG0Z4.BlFNSKeQYETyL3..5/ZuFwGb6', 'customer'),
(81, 'Sri', 'sri@gmail.com', 'Abdesir', '089162940952', '$2b$12$LIwDhXbNUxEhe7.A1c2nsuYqziAMPGggdChe8Jf1zRshB.0LVvjWC', 'customer'),
(82, 'Gebby', 'gebby@gmail.com', 'Perintis', '085107211267', '$2b$12$KohP/./QCp1Dmi1Le2FKUehceLMXEnDg.S8z2xahiUbz1h4blWSM6', 'customer'),
(83, 'Eny', 'eny@gmail.com', 'btp', '086124478727', '$2b$12$AZuHREp9CUYS0oA1s3JJrupm4l7jkToBRNI36BpQKVpq58O3ftOf2', 'customer'),
(84, 'iska', 'iska@gmail.com', 'jl sahabat', '088198611914', '$2b$12$NNJghiAR5xHnepW57DgR3uoROTG6rax0Ws0EA5O3Uias5dEtWlEtC', 'customer'),
(85, 'nani', 'nani@gmail.com', 'tallo', '088272666896', '$2b$12$By/2dU.jMXggKppkmY4SGOIQjFZUsIrsgrP0NLyNBgb.2kWL55Swy', 'customer'),
(86, 'Ramdhana', 'ramdhana@gmail.com', 'Perintis', '087655613339', '$2b$12$B4zeJtmSpKw5lz05EVmbnuC7bhb..yWSt0PD4BshgX.OecuJXfuk2', 'customer'),
(87, 'Rusniati', 'rusniati@gmail.com', 'Perintis', '087120866717', '$2b$12$rLHoI0D69Q.OOBMtrxzZFOZWFiHthe6pR/4gJCZo4rBLjnOJ6aJcO', 'customer'),
(88, 'Fatmawati', 'fatmawati@gmail.com', 'Btp', '081898478187', '$2b$12$RkgCwAvJptaYKaZQhoE2he8RdKjGvVFCyNahYvjVwUGtGP3GREFmC', 'customer'),
(89, 'Nur eny', 'nur.eny@gmail.com', 'Btp', '084008815722', '$2b$12$Y8je.Liwrjip3h1bP0446O0cKLzEcgiqBiueGkm.L5IPckw/lOGu.', 'customer'),
(90, 'Dian', 'dian@gmail.com', 'Alauddin', '089805354951', '$2b$12$kO9jklj0997Miqkz8s18s.bFjwanG2emoL07hBBgin8e6n6Rk6whS', 'customer'),
(91, 'Andi', 'andi@gmail.com', 'Batua', '084828212551', '$2b$12$j0V2dedE2U55aO9FP2mDzuPLRyfVoo4Vgez0xoKvB9lDk6VDAWq6y', 'customer'),
(92, 'Firda', 'firda@gmail.com', 'Borong', '088587257471', '$2b$12$r/L3BxFQDSUn.JEkWFlESuN/tQHaxVSoc/RILK8i0uGI9VC/h1tXq', 'customer'),
(93, 'Faziah', 'faziah@gmail.com', 'Pengayoman', '088458440459', '$2b$12$cXUNsM.Ee8M4L5QsmJbv6eFlUHh9j1dvtXuJ51c2ewiexjDIPbygK', 'customer'),
(94, 'Fiqa', 'fiqa@gmail.com', 'Hertasning', '082883314410', '$2b$12$nTuU/5uLA75fU36Mojq7QeJjgsd5MfCgYgeAey4EvMw87BzDRJQKO', 'customer'),
(95, 'Fita', 'fita@gmail.com', 'Samata', '084247780967', '$2b$12$uT4Qr7mhhzLIuAKKp0OAiemQC.R.AWletUc6nNDk9K9xx7xANXtD6', 'customer'),
(96, 'Tita', 'tita@gmail.com', 'Abdesir', '087212451701', '$2b$12$GOD1HDCA8QD0zs.Pf43TperO/yErdQxk/Ds.RPJDtvLCZyA9uNdMy', 'customer'),
(97, 'Itha', 'itha@gmail.com', 'Perintis', '081599548689', '$2b$12$hUMmCI0yPFhRvt4fBOwivuODCN9iIjtBYtZhYAwbPzDTtjYeAfpAu', 'customer'),
(98, 'Nursepti', 'nursepti@gmail.com', 'Perintis', '084589924283', '$2b$12$eADRqJB4oCggCdDLwh6JFe6sikcz7hn.BctBwGpHim8y556m2JT8m', 'customer'),
(99, 'Nurlaela', 'nurlaela@gmail.com', 'Perintis', '088232484370', '$2b$12$yo/zdVI9YMI8w.CBucaKV.gb.2x8BDj2jM52HWqEV32fITH4f/3Iu', 'customer'),
(100, 'Nurlian', 'nurlian@gmail.com', 'Perintis', '084533327342', '$2b$12$X4LINHmN4lnek9u0jEP9F.ufhX7BXjtmpk3/NAuX06PFzQN8M39Pi', 'customer'),
(101, 'Titi', 'titi@gmail.com', 'Perintis', '083369495565', '$2b$12$uZvfr1hkb9aPG9vjV2fRaehHcWC8k.USPiTu8yq6b10p8OG9xt.WO', 'customer'),
(102, 'Aini', 'aini@gmail.com', 'Btp', '084825792393', '$2b$12$QLB7Wb3Ahf5XlUu3zLQX2eTD1qoCJnOKfjcHNcTj0.2IZdNJG7lOa', 'customer'),
(103, 'Alya', 'alya1@gmail.com', 'Tallo', '086159844316', '$2b$12$opB6ERolEzrSgIw0os69MuLCphL.hWlIGjmwNaSLv8Ak8Qo4ahhC2', 'customer'),
(104, 'Irawati', 'irawati@gmail.com', 'Antang', '081521074575', '$2b$12$5mPKwQan2pLm/uMVbrPCYelqKEE3y7TT5H/vnXA1Twy28PfM5axVS', 'customer'),
(105, 'Lisa', 'lisa3@gmail.com', 'Abdesir', '082150948594', '$2b$12$/7NbI9MjQxPkasovKVr98eJhtkXxJNU86XuizZcoqBJfZAoIJQ1Qq', 'customer'),
(106, 'Nurfadillah', 'nurfadillah@gmail.com', 'Perintis', '085362194309', '$2b$12$H7X7cp7OQIg5ss.zEWJ7TOtY.LQXp6O0KEcWJehUcOIjJxqMyNPZ.', 'customer'),
(107, 'Vinni', 'vinni@gmail.com', 'Tallo', '081870434190', '$2b$12$YaDetEZAynizKZ/rpN2NTe9r6RQoDLawtGXiWt2qvLE8BliGrV6vW', 'customer'),
(108, 'Dany', 'dany@gmail.com', 'Urip Sumoharjo', '083634149130', '$2b$12$JNoRMwRt/kH9AozCnOMZ8uoZ05dDBlGI5O21YJ7ErRZV9sqvxtzKq', 'customer'),
(109, 'Rezkianti', 'rezkianti@gmail.com', 'Veteran', '088924991981', '$2b$12$d8UQm61Icg3h7ydI.kztBezerH96cpuP0OgjYLHedsw6fMZkOZyyW', 'customer'),
(110, 'Nursyakina', 'nursyakina@gmail.com', 'Bandang', '080548618153', '$2b$12$0haOFRUnQwmumYY/UP8nauZf7MwfRx4aTtG.w9lv0GGzmL2syuUkC', 'customer'),
(111, 'Ana', 'ana@gmail.com', 'Baji Minasa', '087188354717', '$2b$12$vbDhrzpD2wvYMeQ5IRsgo.JWzpgwHbB6Wm/uDk9WyNmDBZHecssCa', 'customer'),
(112, 'Wisma', 'wisma@gmail.com', 'Bandang', '085584261618', '$2b$12$aagwgquV4KyHQ4vaZKTjHOHPZ1opWJMwy/MQzeMtQbzPh6zK0M0tG', 'customer'),
(113, 'Fitriah', 'fitriah@gmail.com', 'Bandang', '086072369403', '$2b$12$oNgqH9oUWfeQ5W6bxl5Pcuuw0Q4yWpwBff1H6QpZiPTr/QIgDkAAC', 'customer'),
(114, 'hanifa', 'hanifa@gmail.com', 'Gagak', '089711990367', '$2b$12$RG2LkzEDHpAGW1B0LDD8NeRnRwreUulLDyhSr.d3FICuNFnahcCiG', 'customer'),
(115, 'Saripa', 'saripa@gmail.com', 'cendrawasih', '086454120083', '$2b$12$A3y5b75MftbotL79ScUZqeGSXBvlMeMfXv50k3BukVB9x5nzebe8O', 'customer'),
(116, 'Vira', 'vira@gmail.com', 'cendrawasih', '089828918625', '$2b$12$OFzRZ796N5QiQ0rduITV5O42F7K4CBSe7rBIMsu/HV6GhVqsM3kVu', 'customer'),
(117, 'Ferawati', 'ferawati@gmail.com', 'Talasalapang', '087878514786', '$2b$12$ITPOr9arLMtlhaTnP0446eB5Sd1VrW6TsHQeEATC00Ylq/H/vK1Wu', 'customer'),
(118, 'Nurul', 'nurul1@gmail.com', 'Talasalapang', '080669954740', '$2b$12$COCGkH1/SidhaoQAKT2tMeXdvMtYh9e4pBDES54ReddQIkraytKKO', 'customer'),
(119, 'Rahma', 'rahma@gmail.com', 'Talasalapang', '081545334558', '$2b$12$e8p7XfGJgA2MSMcsJ26DaeFwGQWS8WJz9wRFifgIqdAfDkwTqsn6q', 'customer'),
(120, 'Nahdatul', 'nahdatul@gmail.com', 'Btp', '085326864460', '$2b$12$RGDZ929aeUFu0eUqRuM.9.ErQwEBra0E.xNMVJ8RyTK4rRyT7.0GW', 'customer'),
(121, 'Pricilia', 'pricilia@gmail.com', 'Baruga', '083894171253', '$2b$12$H4X8RiPRAL2jUtr/TCcC7uDoRKkyOU0TeTwldnirK5QiCvmQ0u3vG', 'customer'),
(122, 'Eden', 'eden@gmail.com', 'Tamangapa', '089272530471', '$2b$12$WAfMDV0wmw7jFyWuUfrjAuAE3Awmn.o09FIyPwqOAXzw9tRXlOtj.', 'customer'),
(123, 'Andi amalia', 'andi.amalia@gmail.com', 'Tamangapa', '083830106590', '$2b$12$u6kv7V.tPE/UcKSbkPftme1XCyvJAwYhIRD6yitn.LgXdzBtvAlA2', 'customer'),
(124, 'Ira', 'ira@gmail.com', 'Perintis', '088470767658', '$2b$12$8472PTFmGAwI/Ajs0m4.1.HC4sFxVaqsd8/tvdQGAGTc/4fz/0luG', 'customer'),
(125, 'Thifa', 'thifa@gmail.com', 'Telkomas', '081368404630', '$2b$12$WYNzwFYfsnArkAtvb6RMXOhkJq0iXQn/w8XF.Ot9AZ/M6CZfXpN5a', 'customer'),
(126, 'Wahida', 'wahida@gmail.com', 'Moncongloe', '083826787029', '$2b$12$ClO4jLf2SwDBQsqDWbW0de/dIbwso8DA4.ZNBINzDU1Q0iVWRVMdK', 'customer'),
(127, 'Fia', 'fia@gmail.com', 'Hertasning', '084604244480', '$2b$12$ZPyqt2876RFz/n747HsvEeZOEDJmXGShgmOxcBYcRbfF9Cgc/Zumq', 'customer'),
(128, 'Annisa', 'annisa@gmail.com', 'Toddopuli', '080692391955', '$2b$12$YG6bOoJyJwqoT8VOSw7lH.0/SFBSXQwxuHxkfuNB4Cy7tDH2cSPAO', 'customer'),
(129, 'Rostati', 'rostati@gmail.com', 'Kima raya', '080995215220', '$2b$12$jDIuA1noCcmuk2TQ2lyzSu4Vn7sl8hiYfMQw3RW3Vn0jAJ7w/8U1.', 'customer'),
(130, 'Eka', 'eka1@gmail.com', 'Kima raya', '081993965608', '$2b$12$7aR1L1ENcjcB8qfNmFWi0ezGyNqZ20L75iDQknO0A2kdp9vKVduOO', 'customer'),
(131, 'Qadriah', 'qadriah@gmail.com', 'Urip Sumoharjo', '085229145127', '$2b$12$Casmn3sYr6ydMYQ.HO9b1OT4hcmDuILRCbL/JbfwGWuFgZhJpZ.Pe', 'customer'),
(132, 'Sri dewi', 'sri.dewi@gmail.com', 'Batua', '085599218196', '$2b$12$5mS1Yb4SIS1bjasdUiXvL.AEp407g6XwUixx6uEB6QWtRThN850/.', 'customer'),
(133, 'Ariani', 'ariani@gmail.com', 'Banta bantaeng', '082434832735', '$2b$12$iDwXoCmuaF5rqkMiKK9Y4uAJUovusFDHJTfNzM6K5S4pIgrf40iOi', 'customer'),
(134, 'Ria ramadani', 'ria.ramadani@gmail.com', 'Banta bantaeng', '082896569812', '$2b$12$n50KMen9ipAWFaVZ7pasMOJYKbfqdV7z4ys8f2sGAlTCYQO0Ri5gu', 'customer'),
(135, 'Yuyun', 'yuyun@gmail.com', 'Banta bantaeng', '089604631898', '$2b$12$0tX60qaofInJUA7XDrjUF.CPCaoLue0m4GARm9ayvvi6fPd6QwWZ2', 'customer'),
(136, 'Ria ramadani', 'ria.ramadani1@gmail.com', 'Landak', '083059433695', '$2b$12$ouL2K9O/d6DRLlLhalJFhuVEcowofN1F5x3JHEzarL16rPyBPvSr6', 'customer'),
(137, 'Fiqhi', 'fiqhi@gmail.com', 'Alauddin', '082259727772', '$2b$12$INw21318kJJVKG6s.T6Rc.eLVOamfDiebW3WpPpYzVpBNvW6GnmF6', 'customer'),
(138, 'Irma delin', 'irma.delin@gmail.com', 'Hartaco', '089052502073', '$2b$12$o0sYeZm2tPpJ8sYxuyfuteQgwmOFQE52ShEqLEBH9nOtUJXksIOGC', 'customer'),
(139, 'Irnawati', 'irnawati@gmail.com', 'Hertasning', '080780725877', '$2b$12$yE.bDwfKYAGUZPB.o90lCujg0Wv6iHn7irsK/sp83XsmKgRNy6TpC', 'customer'),
(140, 'Isnayanti', 'isnayanti@gmail.com', 'Pendidikan', '089852994583', '$2b$12$0fBOc0ifgiTz/HkeafUo1O50BflmRLwrQ18J/hzCP9QqI2Koc5h76', 'customer'),
(141, 'Nurul hijja', 'nurul.hijja@gmail.com', 'Veteran', '089921198473', '$2b$12$RsbTNexW8hn0vTcQKHCsB.39uxxcfwigdPEmslUDj/BYwGWOecEfu', 'customer'),
(142, 'Jurana', 'jurana@gmail.com', 'Rappocini', '082610661495', '$2b$12$Vmnio0vUOkXDIQItpGUzo.WQBjK4mOALtZXbVTqNFAPiXUIlkiOFi', 'customer'),
(143, 'Sidra', 'sidra@gmail.com', 'Rappokalling', '089278113120', '$2b$12$D9HVMgmOTaK0fUtf66byle7mWtxRKjjVnzBJU4y087NxkSE.ho8qG', 'customer'),
(144, 'Ariani', 'ariani1@gmail.com', 'Alauddin', '085519135301', '$2b$12$NgVh8xl6NPNPJvkZYOfMfOxTPUY0XSHR8mCfj9odLvbwlULpx/hCS', 'customer'),
(145, 'St Ainun', 'st.ainun@gmail.com', 'Rappocini', '085247174626', '$2b$12$Mz0ySE0e4J23TDXf.2gZSO1BJQcvHguqxgegOXk8mK4oD/UXoamrW', 'customer'),
(146, 'Nurul uswatun', 'nurul.uswatun@gmail.com', 'Rappocini', '087743717536', '$2b$12$bVdtOSW.Jngz8uW7wI5Z1ezDkTL0ulJWEgx90EiLpEfHDSvU2p0e.', 'customer'),
(147, 'Shinta', 'shinta@gmail.com', 'Veteran', '086673507267', '$2b$12$dXBUiNo7PxpmOVv4apHls.bQoo4t3ANRMh1vz1eZXXsWQ9yHsEMbS', 'customer'),
(148, 'Maharani', 'maharani@gmail.com', 'Faisal', '082009005710', '$2b$12$1WJ9fQmi2VtRroOqMqsxDez5yATV/JSlacXe9jlD8PIO5aVDVm7VG', 'customer'),
(149, 'Andi putri', 'andi.putri@gmail.com', 'Antang', '086620031111', '$2b$12$QZSK62bivTB..IFlR9H/bewhr0aiwO7chnWHOuOodMZgKERojam3u', 'customer'),
(150, 'Astira', 'astira@gmail.com', 'Btn Antara', '085623406757', '$2b$12$mvAKZslLyOfWg3nuVJg8.OYSndFotYd.1DQ7d6jB4.CJTECuxwoXS', 'customer'),
(151, 'Firda', 'firda1@gmail.com', 'Perintis', '081691250782', '$2b$12$AYjowgfEguwvS8wjmFk.F.iYB7JIHx02QDLJpw7gMot71xzXY.736', 'customer'),
(152, 'Risda', 'risda@gmail.com', 'Btp', '085025460309', '$2b$12$gvy6rSOoQYwff2ruANPZieQ9FhIXoCJppMyDebAm6TO0qXBs3eJm.', 'customer'),
(153, 'Fatimah', 'fatimah@gmail.com', 'tallo', '086901768387', '$2b$12$LCjoMUZdP9gly3Q05k.XY.z4DFeqQNV8HI.5EwybtuRVvQn/J8K3K', 'customer'),
(154, 'Irma', 'irma@gmail.com', 'Rappocini', '086375169427', '$2b$12$oB9xWtI9KibZfoBOP5bwtOXV/lmB1d188IFV..T3vzjo7nVaLvWPK', 'customer'),
(155, 'Hafia', 'hafia@gmail.com', 'Btp', '085365900995', '$2b$12$nmutmPw42dmgsOAsKXqsmuvhxMuUv99Xn/C4PqnpBU3AsQQNhPtqO', 'customer'),
(156, 'Wahidah', 'wahidah@gmail.com', 'Talasalapang', '081282391077', '$2b$12$Zk412NIpeJcjEYPLLvwfse0ws5HIrp8sU3c9HR1hRc0.6NDYb/pXy', 'customer'),
(157, 'Khaerunnisa', 'khaerunnisa@gmail.com', 'Maccini', '087071597298', '$2b$12$07duXmRe8HTCmjhsw58eHuo/s11u8bkzv2dYLvqPtvdejRUSY4eZS', 'customer');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_users_email` (`email`),
  ADD KEY `ix_users_id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=158;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

create database batcomputer;

use batcomputer;

create table tarefas(
	tar_id int primary key auto_increment,
	tar_nome varchar(30) not null,
	tar_materia varchar(30),
	tar_status varchar(30),
	tar_data_conclu date,
    tar_tipo varchar(20) not null,
    constraint ck_tarefa_tipo check (tar_tipo in ('Faculdade', 'Projeto')),
	constraint ck_tarefa_status check (tar_status in ('Pendente', 'Em andamento', 'Concluido'))
);

select * from tarefas;

INSERT INTO tarefas (tar_nome, tar_materia, tar_status, tar_data_conclu, tar_tipo)
VALUES 
('Questionario', 'Banco de dados', 'Pendente', '2026-09-30', 'Faculdade'),
('Batcomputer', NULL, 'Em andamento', NULL, 'Projeto');
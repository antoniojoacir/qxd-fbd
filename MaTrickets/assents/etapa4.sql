-- Criando Visões

create or replace view detalhes_tickets as
select
    t.id_ticket,
    t.numero,
    t.lote,
    c.id_cliente,
    c.cpf as cpf_cliente,
    c.pnome as nome_cliente,
    c.unome as sobrenome_cliente,
    e.id_evento,
    e.titulo as nome_evento,
    e.data_inicio,
    e.data_fim,
    e.horario_inicio,
    e.horario_fim
from
    tickets as t
left join
    clientes as c 
	on t.id_cliente = c.id_cliente
left join
    eventos as e 
	on t.id_evento = e.id_evento


create or replace view detalhes_eventos as
select
    e.id_evento,
    e.titulo,
    e.data_inicio,
    e.data_fim,
    e.horario_inicio,
    e.horario_fim,
    count(distinct t.id_ticket) as tickets_vendidos,
    count(distinct a.id_atracao) as atracoes
from
    eventos as e
left join
    tickets as t 
	on e.id_evento = t.id_evento
left join
    se_apresenta as a
	on e.id_evento = a.id_evento
group by
    e.id_evento

select * from detalhes_eventos




--Criando usuários e permissões


create user user_admin with password '123456'
grant all privileges on all tables in schema public to user_admin



create user user_leitor with password '123'
grant select on all tables in schema public to user_leitor


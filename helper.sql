-- select Create_Study_Group('Test', 10, 1, 1, '2024-11-20', 10, 2, 1);

create or replace function Create_Study_Group(
    content TEXT,
    user_max BIGINT,
    course_id BIGINT,
    Owner_id BIGINT,
    event_date DATE,
    event_period_start INTEGER,
    event_duration BIGINT,
    classroom_id BIGINT
) returns BIGINT
as $$
declare
    new_event_id BIGINT;
BEGIN
    INSERT INTO "STUDY_EVENT" (Content, Status, User_max, Course_id, Owner_id)
    VALUES (content, 'Ongoing', user_max, course_id, owner_id)
    RETURNING Event_id INTO new_event_id;

    for i in 0..(event_duration-1)
    loop
        INSERT INTO "STUDY_EVENT_PERIOD" (Event_date, Event_period, Classroom_id, Event_id)
        VALUES (event_date, event_period_start+i, classroom_id, new_event_id);
    end loop;
    return new_event_id;
END;
$$ LANGUAGE plpgsql;






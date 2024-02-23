alter table "public"."actions" enable row level security;

set check_function_bodies = off;

CREATE OR REPLACE FUNCTION public.delete_last_inserted_row_for_current_user()
 RETURNS json
 LANGUAGE plpgsql
AS $function$ 
DECLARE 
    user_id_param uuid;
    row_deleted integer;
    deleted_record json;
BEGIN 
    user_id_param := auth.uid(); -- Assuming auth.uid() returns UUID

    DELETE FROM public.actions 
    WHERE id = (
        SELECT id 
        FROM public.actions 
        WHERE user_id = user_id_param 
        ORDER BY created_at DESC 
        LIMIT 1
    ) 
    RETURNING json_build_object('action', action, 'timestamp', time) 
    INTO deleted_record;

    GET DIAGNOSTICS row_deleted = ROW_COUNT;

    IF row_deleted > 0 THEN 
        RETURN deleted_record; 
    ELSE 
        RETURN '{"message": "No record deleted"}'; 
    END IF; 
END; 
$function$
;

create policy "Only authenticated users can insert."
on "public"."actions"
as permissive
for insert
to authenticated
with check (true);


create policy "User can delete own row"
on "public"."actions"
as permissive
for delete
to authenticated
using ((user_id = auth.uid()));


create policy "User can select own row"
on "public"."actions"
as permissive
for select
to authenticated
using ((user_id = auth.uid()));




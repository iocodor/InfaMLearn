CREATE OR REPLACE Procedure TEMP_OMKAR_SEQ_GEN_V2
IS
   v_LOP NUMBER;
   v_DEP NUMBER;
   v_RES NUMBER;
   v_OWNAME VARCHAR(200);
   v_OBJNAME VARCHAR(200);
   v_OBJTYPE VARCHAR(200);
   v_CON NUMBER;
   v_DDLTXT CLOB;
   v_GRANT CLOB;
   v_RCONS CLOB;
   v_NRCONS CLOB;
   v_DDLTYPE VARCHAR(200);
   v_DRES CHAR(1);
   v_RDEP NUMBER;
   v_RRES NUMBER;

   CURSOR cur_OBJ IS
   SELECT   OWNER_NAME
            ,OBJECT_NAME
			,OBJECT_TYPE
            ,DRES
   FROM   TEMP_OMKAR_OBJECTS 
   WHERE  DRES = 'N';

BEGIN
  v_CON := -1;
  v_LOP := 1;
  WHILE v_CON!=0
  LOOP
    OPEN cur_OBJ;
      LOOP
        FETCH cur_OBJ INTO v_OWNAME,v_OBJNAME,v_OBJTYPE,v_DRES;
        EXIT WHEN cur_OBJ%NOTFOUND;
		
          v_DDLTXT := '-1';
          v_GRANT := '-1';
		  v_RCONS := '-1';
		  v_NRCONS := '-1';	
		  
          SELECT  COUNT (DISTINCT REFERENCED_NAME) INTO v_DEP
          FROM    ALL_DEPENDENCIES
          WHERE   NAME = v_OBJNAME
          AND     REFERENCED_NAME != v_OBJNAME
		  AND     UPPER(REFERENCED_OWNER) != 'SYS';
          
          SELECT  COUNT(*) INTO v_RES
          FROM    TEMP_OMKAR_SEQ 
          WHERE   OBJECT_NAME IN ( 
                                  SELECT DISTINCT REFERENCED_NAME
                                  FROM    ALL_DEPENDENCIES
                                  WHERE   NAME = v_OBJNAME
                                  AND     REFERENCED_NAME != v_OBJNAME)
								  AND     UPPER(REFERENCED_OWNER) != 'SYS';
			
			
			
			SELECT 	COUNT(*) INTO v_RDEP
			FROM 	ALL_CONSTRAINTS 
			WHERE 	CONSTRAINT_NAME IN(
										SELECT 	R_CONSTRAINT_NAME 
										FROM 	ALL_CONSTRAINTS 
										WHERE 	TABLE_NAME = v_OBJNAME);	 
			SELECT  COUNT(*) INTO v_RRES
			FROM    TEMP_OMKAR_SEQ 
			WHERE   OBJECT_NAME IN (
									SELECT 	TABLE_NAME
									FROM 	ALL_CONSTRAINTS 
									WHERE 	CONSTRAINT_NAME IN(
																SELECT 	R_CONSTRAINT_NAME 
																FROM 	ALL_CONSTRAINTS 
																WHERE 	TABLE_NAME = v_OBJNAME)
									);
                                            
         IF ((v_DEP = 0 AND v_RRES=v_RDEP) OR (V_DEP = V_RES AND v_RRES = v_RDEP)) THEN
                  
            --OBJECT CREATE DDL
            SELECT 	DBMS_METADATA.GET_DDL (PO.OBJECT_TYPE, PO.OBJECT_NAME) INTO v_DDLTXT 
            FROM 	TEMP_OMKAR_OBJECTS PO
            WHERE 	OWNER_NAME = v_OWNAME AND OBJECT_NAME = v_OBJNAME;
            
            -- NON REFERENTIAL CONSTRAINTS
            SELECT	REGEXP_REPLACE(WM_CONCAT(dbms_metadata.get_ddl('CONSTRAINT', c.constraint_name)),',','') INTO v_NRCONS
            FROM  	USER_CONSTRAINTS C 
            WHERE 	C.TABLE_NAME = v_OBJNAME
              AND CONSTRAINT_TYPE != 'R';
            
            -- REFERENTIAL CONSTRAINTS	
            SELECT 	REGEXP_REPLACE(WM_CONCAT(dbms_metadata.get_ddl('REF_CONSTRAINT', c.constraint_name)),',','') INTO v_RCONS
            FROM  	USER_CONSTRAINTS C 
            WHERE 	C.TABLE_NAME = v_OBJNAME
              AND CONSTRAINT_TYPE = 'R';	
              
            --OBJECT GRANT DDL
            SELECT 	REGEXP_REPLACE((WM_CONCAT('GRANT ' || PRIVILEGE || ' ON ' || TABLE_SCHEMA || '.' || TABLE_NAME || ' TO ' || GRANTEE || ';')),',',CHR(10)) INTO v_GRANT
            FROM 	ALL_TAB_PRIVS 
            WHERE 	TABLE_NAME = v_OBJNAME;

			
            INSERT INTO TEMP_OMKAR_SEQ (OWNER_NAME,OBJECT_NAME,OBJECT_TYPE,DDL_TYPE,DDL_TEXT,LVL)
            VALUES (v_OWNAME,v_OBJNAME,v_OBJTYPE,'CREATE',v_DDLTXT,v_LOP);
			
            IF (v_NRCONS IS NOT NULL) THEN
              INSERT INTO TEMP_OMKAR_SEQ (OWNER_NAME,OBJECT_NAME,OBJECT_TYPE,DDL_TYPE,DDL_TEXT,LVL)
              VALUES (v_OWNAME,v_OBJNAME,v_OBJTYPE,'NRCONSTRAINT',v_NRCONS,v_LOP);
            END IF;
            
            IF (v_RCONS IS NOT NULL) THEN
              INSERT INTO TEMP_OMKAR_SEQ (OWNER_NAME,OBJECT_NAME,OBJECT_TYPE,DDL_TYPE,DDL_TEXT,LVL)
              VALUES (v_OWNAME,v_OBJNAME,v_OBJTYPE,'RCONSTRAINT',v_RCONS,v_LOP);
            END IF;
            
            IF (v_GRANT IS NOT NULL) THEN
              INSERT INTO TEMP_OMKAR_SEQ (OWNER_NAME,OBJECT_NAME,OBJECT_TYPE,DDL_TYPE,DDL_TEXT,LVL)
              VALUES (v_OWNAME,v_OBJNAME,v_OBJTYPE,'GRANT',v_GRANT,v_LOP);
            END IF;
			
            UPDATE  TEMP_OMKAR_OBJECTS
               SET  DRES = 'Y'
             WHERE  OBJECT_NAME = V_OBJNAME
               AND  OWNER_NAME = v_OWNAME;
                
          /*ELSIF(V_DEP = V_RES AND v_RRES = v_RDEP) THEN
             INSERT INTO TEMP_OMKAR_SEQ (OWNER_NAME,OBJECT_NAME,LVL)
             VALUES (v_OWNAME,v_OBJNAME,v_LOP);
             UPDATE  TEMP_OMKAR_OBJECTS
              SET   DRES = 'Y'
              WHERE OBJECT_NAME = v_OBJNAME
                AND OWNER_NAME = v_OWNAME;*/
          END IF;
     END LOOP;
    CLOSE cur_OBJ;
    COMMIT;
    
     SELECT   COUNT(*) INTO v_CON
     FROM     TEMP_OMKAR_OBJECTS 
     WHERE    DRES = 'N';
     V_LOP := V_LOP+1;
     IF V_LOP = 100 THEN
        EXIT;
      END IF;     
  END LOOP;
EXCEPTION
WHEN OTHERS THEN
   RAISE_APPLICATION_ERROR(-20001,'An error was encountered - '||SQLCODE||' -ERROR- '||SQLERRM);
END;
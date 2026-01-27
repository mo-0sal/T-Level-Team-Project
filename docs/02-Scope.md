- **Inscope**
- User login(manager,user)
- dashboard/manager dashboard
- work status
- filter/search(for example, search for a task/who assigned for task/a employee and who they are assigned for)
- permission control page/list and being to set permission( only allow people to see and controll list/page)



- **out of scope**
- Task/project history 
- sentive employee storage(HR)
- Intregration to third party
- payroll system

-**Timeline** 
- Phase 1 - Analysis of project
- Requiments of system, Success critria, some understanding
- Phase 2 - Design system
-  Use-cases, user stories, DFD, ERD, data dictionary, wireframes, architecture  
- Phase 3 – Build:
- Implement main features in logical order 
- Phase 4 – Test:
- Test plan + test cases + fix log 
- Phase 5 – comfirmation:
- Technical documentation + user guide + presentation + evulation

- **User story**
- Work story - As a staff member, I want status window to show the current state of a task so these task so as a staff memberI can see if a task is completed or needs to be work too.
- Dash board - As a Manager/staff member, I want a dashboard to show current/completed task or project, who has completed the task/project, who is currently assigned to a task/project, see a deadline for task,project so I can manage these task/project or see my task I need to complete.
- Filter/search - As a staff member or manager, I want to able to filter out unnecessary task which don't involve me or as a manager to filter out task to see task I need to see so I can
- Task/project creation/remove - As a manager, I need to be able to create a task/remove a task with certain details(deadline,assign,etc) so I can manage new and old task/projet for staff.
- Task assigned - As a staff member, when I log in, I can see my task in a list/page in a deciated area with deadline next to my assign task and status so I'm able to see my task wihtout filter/search and save time.
- Task history - As a manager, I can see the prevously compeleted task/project so I know what have been done so I don't double complete a task and taste money and time
- Permission histoty - as a manager, I can see permissions of each user/control their permission on a list/page so I can manage/update when they are demoted/promoted and just see current accessible for each staff member.
- User login - As a staff/manager - I can see login in with a spefic login details to the system safely so I can login into the system.
- Intregration to third party - As a manager/staff member, I can access/use third party system/tools within the system to enchance and improve productivity and performance of the system so I can use useful third party tools/system. 

**Risk register** 
Risk ID | Risk     | Impact  | Likelihood | Mitigation
-01| Scope grows| High| Medium| MoSCoW + changes log
-02| Data sensitivity mishandled| High| Low/Med| Roles + least-access control + validation
-03| Interation complexity| Medium| Medium| Keep MVP standalone, links only
-04| Testing left late| Medium| Medium| Write test cases early; test per

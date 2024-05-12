from fastapi import Body, FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import database,schemas,models,oauth2
from sqlalchemy.orm import Session
router=APIRouter(
    prefix="/vote",
    tags=['Vote'],
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,
         db:Session=Depends(database.get_db),
         curr:int=Depends(oauth2.get_current_user)):
    
    post_check=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post Not Found")
    vote_check=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,
                                     models.Vote.user_id==curr.id)
    found_vote=vote_check.first()
    if(vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                               detail=f"user {curr.id} has already voted on {vote.post_id}")
        new_vote=models.Vote(post_id=vote.post_id,
                             user_id=curr.id)
        
        db.add(new_vote)
        db.commit()
        return {"message":"Vote added"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote not found")
        
        vote_check.delete(synchronize_session=False)
        db.commit()
        return {"message":"Successfully deleted vote"}
    
        
        
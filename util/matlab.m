

clear all

%%
data=oommf2matlab(['m000006.ovf']);



datam=oommf2matlab('ground_state_m.ovf');


zs=1;
for i = 1:data.xnodes
    for j = 1:data.ynodes
        bmag(i,j)=(data.dataz(i,j,zs)-datam.dataz(i,j,zs))^2+...
            (data.datax(i,j,zs)-datam.datax(i,j,zs))^2;
        bph1(i,j)=(data.dataz(i,j,zs)-datam.dataz(i,j,zs));    
    
    %sqrt((data.datax(i,j,zs))^2+(data.datay(i,j,zs))^2);
    end
end

bmagh=abs(hilbert(bmag));


%blur log
figure
%Create Gaussian Filter
G = fspecial('gaussian', [400 200], 4);
colormap(jet)
% Blur Image
blurredImage = imfilter(abs(1./(log10(bmag(:,:)).^2)),G,'same');
cmin=9e-4;
cmax=8e-4;
img=pcolor(blurredImage(:,:)'); 
shading interp;


caxis([cmin cmax])
colormap(jet)
colorbar
%xlim([800 3500])
 
